#!/usr/bin/python

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

	#parsing string with several groups or templates
	def parsestr(self, str, itemid, char ):
		count=0
		ib=0
		k=0
		newstring=[]
		for i in range(0,len(str)):
			if str[i]==char:
				count+=1
				newstr=''
				for j in range(ib,i):
					newstr = newstr + str[j]
				newstring.insert(k,newstr)
				k+=1
				ib=i+1
		newstr=''
		for j in range(ib,i+1):
			newstr = newstr + str[j]
		newstring.insert(k,newstr)

		tempstring=()
		#if only 1 item
		if i == 0:
			newstring.insert(0,str)
	#creating groups and templates string for passing to json
		for i in range(0,count+1):
			tempstring=tempstring+({itemid:newstring[i]},)

		return tempstring
 
	#outputs existing hosts, groups, templates
	def zabbixlist(self):
		pattern='*'
		output='extend'

		hostids=zapi.host.get({"output":output, 'search':{'groupids':pattern}})
		print '\n \n', 'Here are available hosts:'
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
	
	#parses string for macros
	def macrosparse(self, str, char1, char2):
		count=0
		ib=0
		k=0
		newstring=[]
		for i in range(0,len(str)):
			if (str[i]==char1) or (str[i]==char2):
				count+=1
				newstr=''
				for j in range(ib,i):
					newstr = newstr + str[j]
				newstring.insert(k,newstr)
				k+=1
				ib=i+1
		newstr=''
		for j in range(ib,i+1):
			newstr = newstr + str[j]
		newstring.insert(k,newstr)

		return newstring

	#returns string for adding macroses
	def zabbixaddmacros(self, macroslist,hostid):
		macrosstr=[]
		i=0
		while i<len(macroslist):
			macroslist[i]='{$'+macroslist[i].upper()+'}'
			macrosstr.append({'macro':macroslist[i],'value':macroslist[i+1]})
			i+=2
		return macrosstr
