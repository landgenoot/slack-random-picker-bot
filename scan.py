#!/usr/bin/env python
# Run as root, otherwise mac addresses will not be collected

import sys
import os
import nmap
import json
import random

# Define users in the following data structure
users = {
  'AC:5F:3E:6E:XX:XX' : 'Daan',
  '00:17:88:13:XX:XX' : 'Jan',
  '00:17:88:13:XX:XX' : 'Piet',
}

nm = nmap.PortScanner()
nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE')

hosts_list = [(x, nm[x]['addresses']) for x in nm.all_hosts()]
mac_addresses = []

# Gather mac addressses
for host in hosts_list:
  if 'mac' in host[1] and host[1]['mac'] in users:
    mac_addresses.append(host[1]['mac'])

# Pick random mac address and show the name belonging to it
random.shuffle(mac_addresses)
if len(mac_addresses) > 0:
  print(users[mac_addresses[0]])
else:
  print("Nobody available")

