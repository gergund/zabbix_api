#!/usr/bin/env python

from zabbix_methods import *
import getopt
import traceback

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-lh', '--listhosts', help='displays list of available hosts', action='store_true')
parser.add_argument('-lg', '--listgroups', help='displays list of available groups', action='store_true')
parser.add_argument('-lt', '--listtemplates', help='displays list of available templates', action='store_true')
parser.add_argument('-n', '--hostname', help='hostname:<name>')
parser.add_argument('-d', '--dns', help='DNS') 
parser.add_argument('-i', '--ip', help='ip address') 
parser.add_argument('-p', '--port', help='port zabbix agent is listening on')
parser.add_argument('-u', '--useip', help='1 or 0. connect to host by IP(1) | DNS(0)') 
parser.add_argument('-g', '--groups', help='comma-separated groups id or names')
parser.add_argument('-t', '--templates', help='comma-separated template ids or names')
parser.add_argument('-m','--macros', help='Macroses list. For example: macro1=value1,...,macroN=valueN') 
#help = 'Actually creating host. Macro are optional parameters', nargs='?')
args = parser.parse_args()

if len(sys.argv)<2:
	parser.parse_args(['-h'])

#print bold+'\nExample: ./zabbix_host_add.py hostname:test dns:hostname.com ip:10.0.0.1 port:10050 useip:1 groups:10011,Linux,"test servers" templates:10026,10027,"new template" macros:macro1=value1,newmacro=newvalue'+reset

zmeth=ZabbixMethods()

list = False
if args.listhosts:
	print 'Current log level is',str(loglevel)+',','you may increase it'
	ids = zmeth.getlist('host')
	ids = [ x['host'] for x in ids ]
	list = True
elif args.listgroups:
	ids = zmeth.getlist('group')
	ids = [ x['name'] for x in ids ]
	list = True
elif args.listtemplates:
	ids = zmeth.getlist('template')
	ids = [ x['name'] for x in ids ]
	list = True
	
if list:
	for i in ids:
		print i
	sys.exit()

args=args.__dict__

templist=zmeth.parseitems(args)

# form strings for transfer to json
string = zmeth.preparestring(templist)
string['groups'] = zmeth.PrepareGroups(templist)
string['templates'] = zmeth.PrepareTemplates(templist)

try:
	createdhost=zapi.host.create(string)
	if 'hostids' in createdhost.keys(): 
		print bold + '\nHost created sucessfuly\n'+reset
except:
	print bold + 'Server returned error: '+ reset,createdhost['error']['message'], createdhost['error']['data'], traceback.format_exc() 
	sys.exit()
hostid=createdhost['hostids'][0]	

#print 'Current log level is',str(loglevel)+',','you may increase it'

if args['macros']:
	macroslist = zmeth.parsemacros(args,hostid)
	print bold+'ololo'+reset, macroslist
	addmacros = zapi.usermacro.create(macroslist)
