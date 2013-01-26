#!/usr/bin/env python

import sys
from zabbix_api import ZabbixAPI
from zabbix_credentials import *

bold = "\033[1m"
reset = "\033[0;0m"

#check if zabbix server is available
try:
	zapi = ZabbixAPI(server=server, path="", log_level=loglevel)
	zapi.login (username,password)
except:
	print bold+"\nCould'n connect to zabbix. Please check if URL " + server + " is avaiable"+reset
	exit(1)

class ZabbixMethods:
	
	def parseitems(self,args):
		#check for all required parameters
		reqkeys1=["hostname","dns","ip","port","useip"]
		reqkeys2=["groups","templates"]
		wrongargs={}
		novalues=[]

		error=0

		for i in reqkeys1+reqkeys2:
			if not args[i]:
				novalues.append(i)
				error = 1
		if len(novalues)>0:
			print bold+'Following values are requied:'+reset
			for i in novalues:
				print i
			sys.exit()

		for i in reqkeys1+reqkeys2:
			args[i]=args[i].split(',')
		for i in reqkeys1:
			#check for only 1 value for items in reqkeys1
			if len(args[i]) != 1:
				wrongargs[i] = args[i]
		if len(wrongargs) > 0:
			print bold+"Only one value is available for this keys, you use more in following:"+reset
			for i in wrongargs.keys():
				print bold+'key'+reset, i , bold+'and values:'+reset, wrongargs[i]
			error = 1
		if args['macros']:
			macroslist=[]
			for i in args['macros'].split(','):
				print i
				macroslist.append({'macro':'{$'+str(i.split('=')[0]).upper()+'}', 'value':i.split('=')[1]})
			args['macros']=macroslist
		if error == 1:
			sys.exit()
		return args
	
	def preparestring(self,keyvalues):
		string={}
		string['host'] = keyvalues['hostname'][0]
		string['interfaces'] = [{'type':1, 'main':1, 'useip':keyvalues['useip'][0], 'ip':keyvalues['ip'][0], 'dns':keyvalues['dns'][0], 'port':keyvalues['port'][0]}]
		string['templates'] = []
		#for i in keyvalues['templates']:
		#	string['templates'].append({'templateid':i})
		#string['groups'] = []
		#for i in keyvalues['groups']:
		#	string['groups'].append({'groupid':i})
		return string

	def getlist(self, type):
		pattern='*'
		output='extend'

		if type == 'host':
			ids = zapi.host.get({"output":output, 'search':{'groupids':pattern}})
		elif type == 'group':
			ids = zapi.hostgroup.get({"output":output, 'search':{"hostids":pattern}})
		elif type == 'template':
			ids = zapi.template.get({'output':output, "search":{"hostid":pattern}})
		return ids
	
	def PrepareGroups(self, keyvalues):
		#check if there is at least 1 group specified by name
		convert=[]
		nonexist=[]
		result=[]
		for i in keyvalues['groups']:
			if not i.isdigit():
				convert.append(i)
		groups={'names':[],'ids':[]}
		groupslist= self.getlist('group')
		for i in groupslist:
			groups['names'].append(i['name'])
			groups['ids'].append(i["groupid"])
		if len(convert)>0:
			for i in convert:
				if i.lower() in [ x.lower() for x in groups['names'] ]:
					index=[ x.lower() for x in groups['names'] ].index(i.lower())
					result.append( { 'groupid' : groups['ids'][index] } ) 
				else:
					nonexist.append(i)
			if len(nonexist) > 0:
				print bold+"Following groups don't exist in zabbix:"+reset
				for i in nonexist:
					print i
				sys.exit()
		nonexist=[]
		for i in [ k for k in keyvalues['groups'] if k not in convert ]:
			if i not in groups['ids']:
				nonexist.append(i)
			result.append({'groupid' : i})
		if len(nonexist) > 0:
			print bold+"Following group IDs don't exist in zabbix:"+reset
			for i in nonexist:
				print i
			sys.exit()
		return result

	def PrepareTemplates(self, keyvalues):
		#check if there is at least 1 template specified by name
		convert=[]
		nonexist=[]
		result=[]
		for i in keyvalues['templates']:
			if not i.isdigit():
				convert.append(i)
		templates={'names':[],'ids':[]}
		templateslist= self.getlist('template')
		for i in templateslist:
			templates['names'].append(i['name'])
			templates['ids'].append(i["templateid"])
		if len(convert)>0:
			for i in convert:
				if i.lower() in [ x.lower() for x in templates['names'] ]:
					index=[ x.lower() for x in templates['names'] ].index(i.lower())
					result.append( { 'templateid' : templates['ids'][index] } )
				else:
					nonexist.append(i)
			if len(nonexist) > 0:
				print bold+"Following templates don't exist in zabbix:"+reset
				for i in nonexist:
					print i
				sys.exit()
		nonexist=[]
		for i in [ k for k in keyvalues['templates'] if k not in convert ]:
			if i not in templates['ids']:
				nonexist.append(i)
  		if len(nonexist) > 0:
			print bold+"Following templates don't exist in zabbix:"+reset
			for i in nonexist:
				print i
			sys.exit()
		nonexist=[]
		for i in [ k for k in keyvalues['templates'] if k not in convert ]:
			if i not in templates['ids']:
				nonexist.append(i)
			result.append({'templateid' : i})
		if len(nonexist) > 0:
			print bold+"Following template IDs don't exist in zabbix:"+reset
			for i in nonexist:
				print i
			sys.exit()
		return result



	#outputs existing hosts, groups, templates
	def zabbixlist(self):
		pattern='*'
		output='extend'

		hostids=zapi.host.get({"output":output, 'search':{'interfaceids':pattern}})
		print '\n \n', 'Here are available hosts:'
		print hostids[0].keys()
		length = len(hostids)
		maxlen = 5
		for i in range(0,len(hostids)):
			if (len(hostids[i]['host']) >= maxlen):
				maxlen=len(hostids[i]['host'])+2
		print 'Hostid'.ljust(6),'Hostame'.ljust(maxlen),'IP'.ljust(maxlen)
		for i in range(0,len(hostids)):
			print str(hostids[i]['hostid']).ljust(6),str(hostids[i]['host']).ljust(maxlen),str(hostids[i]['ip']).ljust(maxlen)

		groupids=zapi.hostgroup.get({"output":output, 'search':{"hostids":pattern}})
		print '\n \n', 'Here are available groups:'
		length = len(groupids)
		maxlen = 5
		for i in range (0, len(groupids)):
			if (len(groupids[i]['name']) >= maxlen):
				maxlen = len(groupids[i]['name'])+2
		print 'Groupid'.ljust(7),'Group name'.ljust(maxlen)
		for i in range(0,len(groupids)):
			print str(groupids[i]['groupid']).ljust(7),str(groupids[i]['name']).ljust(maxlen)

		templateids=zapi.template.get({'output':output, "search":{"hostid":pattern}})
		print '\n \n', 'Here are available templates:'
		length=len(templateids)
		maxlen = 5
		for i in range (0, len(templateids)):
			if (len(templateids[i]['host']) >= maxlen):
				maxlen = len(templateids[i]['host'])+2
		print 'Templateid'.ljust(11),'Template name'.ljust(maxlen) 
		for i in range(0,len(templateids)):
			print str(templateids[i]['hostid']).ljust(11),str(templateids[i]['host']).ljust(maxlen)
		return output

	#search host by IP
	def zabbixhostsearch(self, ip):
		hostids=zapi.host.get({"output":"extend", 'filter':{'ip':ip}})
		if len(hostids) == 1:
			return hostids[0]['hostid']
		else:
			print bold +"\nNothing founded. Please make sure you specified a correct IP \n"+reset

	#parse macros 	
	def parsemacros(self, args,hostid):
		for i in args['macros']:
			i['hostid'] = hostid
		return args['macros']
