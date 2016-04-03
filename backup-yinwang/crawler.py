#!/usr/bin/env python
import re
import urllib
import os

import html2text

html2text.BODY_WIDTH = 0

main_page = urllib.urlopen("http://www.yinwang.org/")
content = main_page.read()
main_page.close()

pattern = re.compile(r'(http://yinwang.org/blog-cn/(201[^"]*))">([^<]+)')
for x in pattern.finditer(content):
    file_name = "yinwang/" + x.group(2).replace('/', '-')[:11] + x.group(3) + ".md"
    if os.path.isfile(file_name):
        print '\033[93m' + file_name + ' exist\033[0m'
        continue
    else:
        print '\033[92m' + file_name + " is new\033[0m"
    sub_page = urllib.urlopen(x.group(1))
    sub_page_content = html2text.html2text(sub_page.read().decode("utf-8"))
    md = open(file_name, "w")
    md.write(sub_page_content.encode("utf-8"))
    md.close()
    sub_page.close()
