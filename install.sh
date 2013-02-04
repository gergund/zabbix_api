#!/bin/bash

VERSION=$1
DIR='zabbix-api'

echo $VERSION

while [[ ("$VERSION" != "1.8") && ("$VERSION" != "2.0") ]]; do
	echo 'Please enter version - 1.8 or 2.0'
	read VERSION
done

if [ ! -d $DIR ]; then
	mkdir $DIR
fi

rm -rf $DIR/*

git submodule init
git submodule update

cp $VERSION/zabbix_methods.py $DIR
cp scripts/zabbix/zabbix_api.py $DIR
touch $DIR/__init__.py

sudo python setup.py install

git update-index --assume-unchanged 1.8/zabbix_credentials.py
git update-index --assume-unchanged 2.0/zabbix_credentials.py

rm -rf zabbix-api/
