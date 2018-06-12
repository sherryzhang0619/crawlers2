# -*- coding:utf-8 -*-

import requests
from lxml import html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#文档目标用来获取最受欢迎影评


K= 0
for k in range(5): #range()从0开始到4，共5个数。
    url = 'https://movie.douban.com/review/best/?start={}'.format(k * 20)
    r = requests.get(url).content
    sel = html.fromstring(r)

    mainreview = sel.xpath('//div[@class="main review-item"]')
    title = sel.xpath('//div[@id="content"]/h1/text()')
    print title[0]

    for i in mainreview:
        reviewer = i.xpath('header[@class="main-hd"]/a[@class="name"]/text()')[0] #从循环的xpath路径下更细化所需要的元素的xpath.
        date = i.xpath('header[@class="main-hd"]/span[@class="main-meta"]/text()')[0] #当print显示的是乱码时可以尝试用[0]来取值
        movie = i.xpath('div[@class="main-bd"]/h2/a/text()')[0]
        comment = i.xpath('div[@class="main-bd"]/div[@class="review-short"]/div[@class="short-content"]/text()')[0]
        comments = comment.replace(" ","").replace("(", "").strip( )

        print reviewer, date, movie, comments

        with open("reviews.txt", "a") as f:
            f.write("标题：%s%s\n评论者：%s\n评论时间：%s\n电影：%s\n影评：%s\n" % (title[0], str(k), reviewer, date, movie, comments))
            f.write("==================\n")

    k = k+1


