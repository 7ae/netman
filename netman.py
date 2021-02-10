import subprocess
import re
import json

def get_interface():
  # Find interface name for wireless hardware
  return _bash('iw dev | awk \'$1 == "Interface" { print $2 }\'')

def scan(interface=None):
  #Scan all networks
  _root()
  return _bash(f'iw {interface if interface else get_interface()} scan')

def parse(scan, associated=False):
  # Parse information from scanned networks
  parse = re.split('^BSS ([a-z0-9:]{17}).*\n\t', scan, 0, re.MULTILINE)
  # Remove empty first element after split
  parse.pop(0)
  cells = []
  for mac, remainder in zip(*[iter(parse)] * 2):
    cells.append({
      'mac': mac,
      'ssid': re.search('(?<=SSID: ).*', remainder).group(),
      'signal': re.search('(?<=signal: ).*(?= dBm)', remainder).group(),
      'frequency': re.search('(?<=freq: ).*', remainder).group()
    })
  
  j = json.dumps(cells, indent=2)
  return j if associated is False else json.loads(j)[0]

def activate():
  # Enable network connection
  _root()
  _bash('nmcli radio wifi on')

def deactivate():
  # Disable network connection and disconnects from current network
  _root()
  _bash('nmcli radio wifi off')

def is_activated():
  # Check if network connection is enabled
  return _bash('nmcli radio all | awk \'FNR == 2 {print $2}\'') == 'enabled'

def connect(ssid, password, interface=None):
  # Connect to a network
  _root()
  nmcli = _bash(f'nmcli device wifi connect {ssid} password {password} hidden yes {interface if interface else get_interface()}')
  return re.search('Device \'\w+\' successfully activated with \'.*\'\.', nmcli) is not None

def disconnect(interface=None):
  _root()
  nmcli = _bash(f'nmcli d disconnect {interface if interface else get_interface()}')
  return re.search('Device \'\w+\' successfully disconnected\.', nmcli) is not None

def is_connected(page='10.0.0.1'):
  ping = _bash(f'ping -c {page} >& /dev/null')
  if len(ping) == 0:
    ping = _bash(f'ping -c 192.168.0.1 >& /dev/null')
  return len(ping) > 0

def _bash(cmd):
  # Check if command exists
  subprocess.check_call(f'which {cmd.split(" ")[0]} &> /dev/null', shell=True)
  p = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return p.stdout.strip()

def _root():
  # Check if user has root privileges
  if _bash('id -u') is not '0':
    raise Exception("must be root")
