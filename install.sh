#!/bin/bash

VERSION=$1

if [ -d zabbix-api ]; then
	mkdir zabbix-api
fi

git submodule init
git submodule update

cp $VERSION/zabbix_methods.py zabbix_api
cp scripts/zabbix/zabbix_api.py zabbix_api
sudo python setup.py install

git update-index --assume-unchanged 1.8/zabbix_credentials.py
git update-index --assume-unchanged 2.0/zabbix_credentials.py
