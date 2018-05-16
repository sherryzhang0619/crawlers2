# -*- coding:utf-8 -*-

import requests #requests是python的一个HTTP客户端库
from lxml import html #lxml是使用Python编写的库，可以迅速、灵活地处理 XML
from lxml import etree
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url1 = 'https://movie.douban.com/chart'

r1 = requests.get(url1).content #request.get().content是用get的方式获取网页的源代码
sel1 = html.fromstring(r1) #调用html.fromstring函数解析html源代码

title1 = sel1.xpath("//h1/text()") #提取h1标签，text()获取该标签下的文本

print type(title1) #查看title的类型
print title1[0] #查看title第一个元素的内容

#爬取排行榜中的电影列表的链接
links = sel1.xpath('//div[@class="pl2"]/a/@href') #查找出排行榜电影列表的链接
movieslink = [] #存放movies的link的列表
for link in links:
    movieslink.append(link)

#爬取排行榜中的电影列表的名称
namelist = sel1.xpath('//div[@class="pl2"]/a/text()') #用xpath来查找排行榜中电影名称
moviesname1 = [] #存放movies的name的列表
for movie in namelist:
    movie = movie.replace(" ", "").replace("\n","").replace("/","") #用replace来替换字符串中的空格、/和换行符
    moviesname1.append(movie)
    if "" in moviesname1:
        moviesname1.remove("") #用remove("")来删除list中的空字符串
json.dumps(moviesname1, encoding='utf-8', ensure_ascii=False, indent=4) #用json.dumps(list, encoding='utf-8', ensure_ascii=False, indent=4)来解决list的中文乱码问题

# 把name与link对应显示在list中
for i in range(len(moviesname1)):
    print moviesname1[i] + " " + movieslink[i]


print "\n"

#爬取排行榜Top250中的电影列表的链接



k = 1
for i in range(10):
    url2 = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25) #设置分页查询

    r2 = requests.get(url2).content
    sel2 = html.fromstring(r2)

    # 所有的信息都在class属性为info的div标签里，可以先把这个节点取出来
    info = sel2.xpath('//div[@class="info"]')

    #当要在某个结点下xpath做循环查询时，可以将结点做为循环的范围
    for i in info:
        #影片名称
        hd = i.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]

        #影片详情
        bd = i.xpath('div[@class="bd"]/p[1]/text()')

        #name = hd[0].replace(" ", "").replace("/", "").replace("\n", "") #hd是一个list，且只有一个值所以用hd[0]来取第一个值
        actors = bd[0].replace(" ", "").replace("/", "").replace("\n", "")
        rate = i.xpath('//span[@class="rating_num"]/text()')[0]
        date = bd[1].replace(" ", "").replace("\n", "").split("/")[0] #split()分隔
        country = bd[1].replace(" ", "").replace("\n", "").split("/")[1]
        comments = i.xpath('//div[@class="star"]/span[4]/text()')[0]

        print "Top%s" % str(k)
        print hd, actors, rate, date, comments, country

        #写入文件：with-as语法with open(filename, mode) as f
        with open("top250.txt","a") as f: # mode=a是追加模式
            f.write("TOP%s\n影片名称：%s\n评分：%s %s\n上映日期：%s\n上映国家: %s\n%s\n" % (k, hd, rate, comments, date, country, actors))

            f.write("====================\n")

        k = k+1
