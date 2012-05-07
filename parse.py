#!/usr/bin/env python26

# Asterisk. Linksys Provisioning
# author: Bova Bovaev <ink08@ink-online.ru> 
#

import os
import re
import sys
import ConfigParser


filename = "/etc/asterisk/custom/sip.conf" # path to sip.conf
work_dir = "/var/lib/tftpboot" # tftp root directory
file_users_mtime = work_dir + "/users_mtime"
config_default = work_dir + "/sample/spa941.cfg.template"


try:
    f = open(file_users_mtime)
except IOError:
    mymtime = ""
except:
    print "unknown error, exit"
else:
    mymtime = f.read()
    f.close()

try:
    mtime = str(os.stat(filename).st_mtime)
except OSError as (errno, strerror):
    print "OS error({0}): {1}: {2}".format(errno, strerror, filename)
    sys.exit(1)
except:
    print "unknown error, exit"

if (mymtime != mtime):
    mymtime = mtime
    f = open(file_users_mtime, 'w')
    f.write(mymtime)
    f.close()
else:
    print "No updates needed, exit"
    sys.exit(0)

config = ConfigParser.ConfigParser()

try:
    config.read(filename)
except IOError as (errno, strerror):
    print "I/O error({0}): {1}: {2}".format(errno, strerror, filename)
    sys.exit(1)

def read_config_value(section, value_name, default_value=None):
    value = default_value
    if config.has_option(section, value_name):
        value = config.get(section, value_name)
    return value

for section in config.sections():
    if config.has_option(section,'mac'):
        mac = config.get(section, 'mac')

        secret = read_config_value(section, 'secret', '')
        fullname = read_config_value(section, 'fullname', '')

        config_mac = work_dir + "/" + "spa" + mac + ".cfg"

        try:
            fin = open(config_default)
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}: {2}".format(errno, strerror, config_default)
            sys.exit(1)

        fout = open(config_mac, "wt")
        for line in fin:
            line = line.replace('|USER|', section)
            line = line.replace('|PASSWORD|', secret )
            line = line.replace('|FULLNAME|', fullname)
            fout.write(line)
        fin.close()
        fout.close()


