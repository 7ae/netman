# Netman
Netman is a network manager for scanning, activating, and connecting to networks.

## Usage

Netman must be run as root.

- [Scanning Networks](#scanning-networks)
- [Connecting to Network](#connecting-to-network)
- [Disconnecting from Network](#disconnecting-from-network)
- [Activating Network](#activating-network)
- [Deactivating Network](#deactivating-network)

### Scanning Networks

`parse()` displays information about all networks.

```python
scan = scan()
parse = parse(scan)
```
Output:
```json
[
  {
    "mac": "aa:bb:cc:dd:ee:ff",
    "ssid": "ATT_2.4G",
    "signal": "-43.00",
    "frequency": "2437"
  },
  {
    "mac": "a1:b2:c3:d4:e5:f6",
    "ssid": "ATT_5G",
    "signal": "-82.00",
    "frequency": "2422"
  },
  {
    "mac": "45:67:89:ab:cd:ef",
    "ssid": "XFINITY",
    "signal": "-76.00",
    "frequency": "2426"
  }
]
```

Use `associated=True` to get information about only current network.
```python
parse = parse(scan, associated=True)
```
Output:

`{'mac': 'aa:bb:cc:dd:ee:ff', 'ssid': 'ATT_2.4G', 'signal': '-43.00', 'frequency': '2437'}`

### Connecting to Network
`connect()` disconnects from current network and attempts to connect to new network.
```python
connect('NETWORK_NAME', 'NETWORK_PASSWORD')
```
You can connect for a specific connection by specifying an interface name.
```python
connect('NETWORK_NAME', 'NETWORK_PASSWORD', 'wlan0')
```
### Disconnecting from Network
`disconnect()` disconnects from current network.
```python
disconnect()
```
You can disconnect for a specific connection by specifying an interface name.
```python
disconnect('wlan0')
```
If computer is connected to a network, `is_connected()` returns `True`. Otherwise, it returns `False`.
### Activating Network
`activate()` enables network connection.
```python
activate()
```
### Deactivating Network
`dectivate()` disables network connection and disconnects from current network. If network connection is disabled, `connect()` instantly fails.
```python
deactivate()
```
If network connection is enabled, `is_activated()` returns `True`. Otherwise, it returns `False`.
