#!/usr/bin/python

from zabbix_methods import *

lenarg=len(sys.argv)
loglevel=1

#if lenarg != 2:
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('<ip>', help = 'Actually creating host. Macro are optional parameters')
args = parser.parse_args()

#else:
ip=sys.argv[1]
zbxsearch=ZabbixMethods()
hostid=zbxsearch.zabbixhostsearch(ip) 
result=zapi.host.delete({"hostid":hostid})
expect={'hostids':[hostid]}
print 'Current log level is',str(loglevel)+',','you may increase it'
if result == expect:
	print bold +"\n"+"Host "+ip+" has been successfuly deleted\n"+reset	 
else:
	print bold +"\n"+"Somethind went wrong. Please check output for errors"+reset
