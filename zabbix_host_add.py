#!/usr/bin/python

from zabbix_methods import *
import getopt

lenarg=len(sys.argv)

if (lenarg != 9) and (lenarg != 8):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', '--list', help='displays list of available hosts, groups and templates', action='store_true')
	parser.add_argument('<hostname> <dns> <ip address> <port> <useip 1 or 0. if 0 - DNS will be used> <groupid1,...,groupidN> <templateid1,...,templateidN> <macro1=value1,...,macroN=valueN>', 
	help = 'Actually creating host. Macro are optional parameters', nargs='?')
	args = parser.parse_args()
	if lenarg == 1:
		parser.print_help()
		print bold+'\nExample: ./zabbix_host_add.py hostname hostname.com 10.0.0.1 10050 1 1,2,3 10026,10027 macro1=value1,newmacro=newvalue'+reset
	if args.list:
		print 'Current log level is',str(loglevel)+',','you may increase it'
		zbxlist = ZabbixMethods()
		zbxlist.zabbixlist()

else:
	tempstr=ZabbixMethods()
	host=sys.argv[1]
	dns=sys.argv[2]
	ip=sys.argv[3]
	port=sys.argv[4]
	useip=sys.argv[5]
	# form strings for transfer to json
	string = {'host':(host),'ip':(ip),'dns':(dns),'port':(port),'useip':(useip)}
	string['groups']=tempstr.parsestr(sys.argv[6], 'groupid', ',')
	string['templates']=tempstr.parsestr(sys.argv[7], 'templateid', ',')
	
	if lenarg == 9:
		macrosstr=sys.argv[8]

	createdhost=zapi.host.create(string)
	try:
		createdhost['hostids']
		print bold + '\nHost created sucessfuly\n'+reset
	except ValueError:
		print bold + '\nError creating host\n'+reset 
	hostid=createdhost['hostids'][0]	

	print 'Current log level is',str(loglevel)+',','you may increase it'

	#check if there are macroses
	if lenarg==9:
		macros=ZabbixMethods()
		macroslist=macros.macrosparse(macrosstr,',','=')

		macrosfinal=macros.zabbixaddmacros(macroslist,hostid)	
		zapi.host.update({'hostid':hostid,'macros':macrosfinal})
