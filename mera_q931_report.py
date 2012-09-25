#!/usr/bin/env python2.6
# -*- coding: utf8 -*-
# author: Bova Bovaev <ink08@ink-online.ru>

from glob import glob
import sys
import re
from collections import defaultdict

codes = defaultdict(int)

try:
    file = glob('/usr/local/mvts/billing/.tmp_log*')[-1]
    lines = open(file).readlines()[-100:]
except (IndexError, IOError):
    sys.exit(2)

lines_len = len(lines)

if lines_len == 0:
    sys.exit(0)

search_regex = re.compile( ur"DISCONNECT-CODE-Q931=(\d+)", re.M | re.S | re.U )

for line in lines:
    match = search_regex.search(line)
    if match:
        codes[match.group(1)] += 1

if (codes['16'] + codes['17'] + codes['18'] + codes['19'])/float(lines_len) < 0.7:
    print "[MERA]: Количество кодов и их количество в последних {0} строках лога:\n\n".format(lines_len)
    for k, v in codes.items():
        print "\tDISCONNECT-CODE-Q931: {0}, Количество: {1} ({2}%)".format(k, v, v*100/lines_len)


