#Zabbix API scripts

##Installation:

cd to repo root<br/>
```bash
cd zabbix_api/
./install.sh <version>
```
version - your zabbix version. Supported: 1.8 for 1.8.* or 2.0 for 2.0.*

###Usage:
Install script will install zabbix_api from https://github.com/gescheit/scripts/tree/master/zabbix/ and zabbix_methods.<br/>
To use scripts in repo, you need only zabbix_methods module:<br/>
```python
from zabbix_api.zabbix_methods import *
```
But, if you need zabbix_api for some reasons:
```python
from zabbix_api.zabbix_api import ZabbixAPI
```

###Changes:

added v2.0<br/>
some minor features could not work, they will be updated soon.<br/>

scripts for v1.8 will be upated soon.<br/>

for v2.0 execute zabbix_host_add.py -h to view help and available options.

<hr>
zabbix_credentials.py - here are username, password, log level and zabbix URL<br/>
zabbix_api.py - a library from https://github.com/gescheit/scripts/tree/master/zabbix/
<hr>
zabbix_host_add.py - creates a host<br/>
zabbix_host_del.py - deletes a host.

Run them both without any arguments to view usage and available options.

<hr>
Useful links:
* http://www.zabbix.com/wiki/doc/api
* http://www.zabbix.com/documentation/1.8/api
* http://www.zabbix.com/forum/showthread.php?t=15218
