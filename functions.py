#!/usr/bin/env python

# vHostX by NoobsCode
# Author: Alexander A. Nordbo
# UR: https://github.com/noobscode

from sys import argv
from os.path import exists
from os import makedirs
from os import symlink
from os import system
import getopt
import os

def help():
	print("""
	Feel free to open an issue on github.
	""")

def header():
	print(r"""

	vHostX By NoobsCode
	https://github.com/noobscode

	""")

def rmsite():
    try:
        input = raw_input
    except NameError:
        pass
    domain=input('input domain to delete: ')
    os.system("rm -fr /var/www/%s"%domain)
    os.system("rm /etc/apache2/sites-enabled/%s.conf"%domain)
    os.system("rm /etc/apache2/sites-available/%s.conf"%domain)
    print('Done!')

def gensite():
    try:
        input = raw_input
    except NameError:
        pass
    serverName = input("Domain: ")
    documentRoot = '/var/www/%s/public_html/' % (serverName)

    def create_vhost(documentRoot, ServerName):
            out = """<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        ServerName %s
        DocumentRoot %s
        <Directory %s>
            Options -Indexes +FollowSymLinks +MultiViews
            AllowOverride All
            Order allow,deny
            Allow from all
            Require all granted
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/%s-error.log
        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/%s-access.log combined
    </VirtualHost>""" % (serverName, documentRoot, documentRoot, serverName, serverName)
            return out

    def wpinstall():
        print('Would you like us to install the latest release of wordpress?')
        ans = input('(Y/N) << ').lower()
        if ans in ['yes', 'y']:
            print('Installing Wordpress...')
            os.system("wget https://wordpress.org/latest.tar.gz")
            os.system("tar -zxvf latest.tar.gz")
            os.system("cp -r wordpress/* %s"%documentRoot)
            os.system("rm -fr wordpress")
            os.system("rm latest.tar.gz")
        if ans in ['no', 'n']:
            pass

    if not os.path.exists(documentRoot):
        os.makedirs(documentRoot)

    if exists('%s/%s.conf' % (documentRoot, serverName)):
            print('vHost already exists. Aborting')
    else:
            target = open('/etc/apache2/sites-available/%s.conf' % serverName, 'w')
            target.write(create_vhost(documentRoot, serverName))
            target.close()

            srcLink = '/etc/apache2/sites-available/%s.conf' % serverName
            destLink = '/etc/apache2/sites-enabled/%s.conf' % serverName
            symlink(srcLink, destLink)

            # User input asking if wordpress is to be installed
            wpinstall()

            # Restart web server service
            system('service apache2 reload')

            # Set and correct permissions
            print('Setting permissions...')
            os.system("chown www-data:www-data  -R /var/www")
