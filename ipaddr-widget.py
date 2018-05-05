# -*- coding: utf-8 -*-
#
# Harmattan IP Address "Widget" (http://thp.io/2011/ipaddr-widget/)
# -----------------------------------------------------------------
# Based on my calendar icon experiment (calenderr.sh), here is someting that
# could provide the community with a way of adding "widgets" to the app screen.
#
# How it works: When clicked, it will automatically update its application icon
# with the current IP(s) from /sbin/ifconfig and the launcher will reload it.
#
# Oh and by the way: The icon update can happen anytime. Next, I want someone
# to come up with an "overlay" icon for their apps to indicate new items (e.g.
# the mail application could have an overlay with the amount of new mails, ...)
#
# Copyright (c) 2011 Thomas Perl <thp.io/about>; License: GPLv3+
#

import Image, ImageDraw, ImageFont
import subprocess
import re
import os

ICON_TEMPLATE = '/home/user/MyDocs/Local/github/mfrasca/ipaddr-widget/template.png' 
ICON_WIDGET = '/home/user/.config/widgets/ipaddr.png'

TARGET_FOLDER = os.path.dirname(ICON_WIDGET)
if not os.path.isdir(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

im = Image.open(ICON_TEMPLATE)
width, height = im.size

ifconfig = subprocess.Popen('/sbin/ifconfig', stdout=subprocess.PIPE)
stdout, stderr = ifconfig.communicate()

ips = re.findall('addr:([^ ]+)', stdout)
ips = [ip.split('.') for ip in ips if not ip.startswith('127.')] or [('Offline',)]
#ips = [('10', '0', '0', '2')] + ips

draw = ImageDraw.Draw(im)
font_path = "/usr/share/fonts/nokia/Nokia Sans/Nokia Sans Semi Bold.ttf"
font_path = "/usr/share/fonts/hack/Hack-Regular.ttf"
font = ImageFont.truetype(font_path, 12)

cols_count = len(ips)
col_width = width / cols_count
for col_no, ip in enumerate(ips):
    rows_count = len(ip)
    row_height = (height-14) / rows_count
    for line_no, part in enumerate(ip):
        sx, sy = draw.textsize(part, font=font)
        draw.text((col_width * col_no + col_width/2 - sx/2,
                   7 + row_height * line_no + row_height/2 - sy/2), part, fill=(255, 255, 255), font=font)
        print(col_no, line_no, part)
del draw

im.save(ICON_WIDGET, 'PNG')

