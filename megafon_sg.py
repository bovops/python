#!/usr/bin/env python

# send sms from megafon service gid.
# author: unknown
#

import urllib
from lxml import etree
from StringIO import StringIO

def get_root(url, params):
    params = urllib.urlencode(params)
    raw_response = urllib.urlopen(url, params).read()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(raw_response), parser)
    root = tree.getroot()
    return root

login='926xxxxxxx'
password='xxxxxxx'

login_url="https://www.serviceguide.megafonmoscow.ru/ps/scc/php/check.php?"
login_params={'CHANNEL':'WWW', 'LOGIN':login, 'PASSWORD':password}
login_root=get_root(login_url,login_params)
session_id = login_root.find(".//session_id").text
lang_id = login_root.find(".//lang_id").text
print 'session_id=',session_id
  
account_info_url="https://www.serviceguide.megafonmoscow.ru/SCWWW/ACCOUNT_INFO?"
account_info_params={'CHANNEL':'WWW', 'P_USER_LANG_ID':lang_id, 'SESSION_ID':session_id}
account_info_root=get_root(account_info_url,account_info_params)
balance=account_info_root.find(".//div[@class='balance_good td_def']").text
print balance

prefix='926'
print 'prefix=', prefix
addr=raw_input('number (7 digits: 1234567): ')
msg=raw_input('message: ')
msg=msg.decode('utf8').encode('cp1251')
sms_url="https://www.serviceguide.megafonmoscow.ru/SCWWW/SUBS_SEND_SMS_ACTION?"
sms_params={'CUR_SUBS_MSISDN': login, 'prefix': prefix, 'addr': addr, 'CHANNEL': 'WWW', 'SESSION_ID': session_id, 'SUBSCRIBER_MSISDN': login, 'MSISDN_TO': prefix+addr, 'P_USER_LANG_ID': lang_id, 'MESSAGE': msg}
sms_root=get_root(sms_url,sms_params)
divs=sms_root.findall(".//div")
for div in divs:
    print div.text.strip()

logout_params={'CHANNEL':'WWW', 'CUR_SUBS_MSISDN':login, 'P_USER_LANG_ID':lang_id, 'SESSION_ID':session_id, 'SUBSCRIBER_MSISDN':login}
logout_url="https://www.serviceguide.megafonmoscow.ru/SCWWW/CLOSE_SESSION?"
logout_root=get_root(logout_url,logout_params)
logout_result = etree.tostring(logout_root, pretty_print=True, method="html")
print logout_result
