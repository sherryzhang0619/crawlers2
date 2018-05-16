# -*- coding:utf-8 -*-

import requests
from lxml import html

#文档目标用来获取最受欢迎影评
url = 'https://movie.douban.com/review/best/'
sel = requests.get(url).content
text = html.fromstring(sel)

title = text.xpath('//div[@id="content"]')
print title





