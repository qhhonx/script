#!/usr/bin/env python
import re
import urllib
import os

import html2text

html2text.BODY_WIDTH = 0
base_folder = "yinwang/"
img_folder = "img/"

main_page = urllib.urlopen("http://www.yinwang.org/")
content = main_page.read()
main_page.close()

img_pattern = re.compile(r'img src="(.*/(.*(?:.jpg|.jpeg|.png|.gif))[^"]*)"')
sub_page_pattern = re.compile(r'(http://yinwang.org/blog-cn/(201[^"]*))">([^<]+)')
for m in sub_page_pattern.finditer(content):
    file_name = base_folder + m.group(2).replace('/', '-')[:11] + m.group(3) + ".md"
    if os.path.isfile(file_name):
        print '\033[93m' + file_name + ' exist\033[0m'
        continue
    else:
        print '\033[92m' + file_name + " is new\033[0m"
    sub_page = urllib.urlopen(m.group(1))
    sub_page_content = sub_page.read()
    images = []
    for match in img_pattern.finditer(sub_page_content):
        images.append(match.groups())
    for img_info in images:
        img_remote = img_info[0]
        img_local = img_folder + img_info[1]
        print '\033[92m' + img_remote + " -> " + base_folder + img_local + "\033[0m"
        urllib.urlretrieve(img_remote, base_folder + img_local)
        sub_page_content = sub_page_content.replace(img_remote, img_local)

    sub_page_md = html2text.html2text(sub_page_content.decode("utf-8"))
    md = open(file_name, "w")
    md.write(sub_page_md.encode("utf-8"))
    md.close()
    sub_page.close()
