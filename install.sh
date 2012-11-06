#!/bin/bash

# b2server

if echo $* | grep -w "\-\-server" > /dev/null 2>&1; then
	mkdir -p /opt/b2project

	rm -rf /opt/b2project/{bin,conf.sample,scheme,db,module}

	cp -R ./b2server/* /opt/b2project/
	mkdir -p /opt/b2project/log;
fi

# b2lib

if echo $* | grep -w "\-\-client" > /dev/null 2>&1; then
	python setup.py install;
fi

# b2webadmin

if echo $* | grep -w "\-\-webadmin" > /dev/null 2>&1; then
	cp ./b2webadmin/httpd.conf /etc/apache2/conf.d/b2webadmin.conf
	cp ./b2webadmin/index.py /usr/bin/b2webadmin.wsgi
	cp ./b2webadmin/static /var/www/b2webadmin;
fi

