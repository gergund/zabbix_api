#!/usr/bin/env python

from zabbix_methods import *

zmeth = ZabbixMethods()
host = zmeth.GetInventory('10.10.219.220')

print host[0]['inventory']['instance_id']

#zmeth.GetDiscovery()
