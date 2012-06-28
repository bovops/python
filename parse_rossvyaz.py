#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
from lxml import etree
import re

page = urllib.urlopen("http://rossvyaz.ru/docs/articles/ABC-4x.html").read()
upage = unicode(page, 'windows-1251')
lines = []

lines.extend(re.findall('<tr>(.+?)</tr>', upage, re.DOTALL))

result = []
result2 = {}

for line in lines:
    td1 = int(re.findall('<td>\t(.+?)\t</td>', line, re.DOTALL )[0])
    td4 = int(re.findall('<td>\t(.+?)\t</td>', line, re.DOTALL )[3])
    td5 = re.findall('<td>\t(.+?)\t</td>', line, re.DOTALL )[4]
    if td1 == 495 or td1 == 499 or td1 == 498:
        result.append([td1, td4, td5])
        if td5 in result2:
            result2[td5] = result2[td5] + td4
        else:
            result2[td5] = td4

for key, value in result2.items():
    print u"{0}\t{1}".format(value, key)



