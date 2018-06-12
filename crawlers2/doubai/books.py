# -*- coding: utf-8 -*-
import requests
from lxml import html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = "https://book.douban.com/tag/?view=type"
r = requests.get(url).content
sel = html.fromstring(r)

#显示豆瓣图书标题
title = sel.xpath('//div[@id="content"]/h1/text()') # title是列表，索引位置是xpath指定的路径，用title[0]可以取到对应的值
print title[0]

#显示豆瓣图书的所有分类：分类 > 子分类
tag = sel.xpath('//div[@class="article"]/div[@class=""]/div[@class=""]') # It refers to all main category blocks.
for i in tag: #遍历所有满足tag的xpath的路径, i也是xpath
    category = i.xpath('a[@class="tag-title-wrapper"]/h2/text()') #指定到满足//div[@class="article"]/div[@class=""]/div[@class=""]/a[@class="tag-title-wrapper"]/h2/text()的路径
    print "category:" + category[0]

    subcategory = i.xpath('table[@class="tagCol"]/tbody/tr/td/a/text()')
    for n in subcategory: #因为每个子标签是在一个table里，同一个xpath下有多个td，所以要再次遍历查找
        print "subcategory:" + n

        url_books = "https://book.douban.com/tag/" + "%s" %n # 用n代入到url里打开新的列表
        r = requests.get(url_books).content
        sel = html.fromstring(r)

        subtitle = sel.xpath('//div[@id="content"]/h1/text()')
        print "subtitle:" + subtitle[0] #每个子分类的标题


        sublist = sel.xpath('//ul[@class="subject-list"]/li[@class="subject-item"]')
        global list
        list = []
        for a in sublist:
            books = a.xpath('div[@class="info"]/h2[@class=""]/a/text()')
            books_name = books[0].replace(" ", "").replace("\n", "")
            score_path = a.xpath('div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')
            # score = float(score_path[0])
            list2 = [books_name, score_path[0]]
            list.append(list2)
            # print str(list2).decode('unicode-escape').replace('u','')
        print str(list).decode('unicode-escape').replace('u','')

            # print books_name, score
        #     list = list.append(list2)
        # print str(list).decode('string_escape')  #用str(list_name).decode('string_escape')来解决list中文不显示的问题







 # str(update_list).decode('string_escape')






