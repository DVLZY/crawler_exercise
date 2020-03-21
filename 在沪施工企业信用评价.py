#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
print('''
在沪施工企业信用评价数据采集器
by 长河落 （52破解）

1、输入总页码和下载起始页就会开始下载
2、会下载到和本程序同一目录下的《在沪施工企业信用评价.txt》 的文件中
3、文件后面的编号是起始下载的页码
4、这个网站有慢，下载的时候要过一会才会写入输入，所以不要着急打开txt文件
''')
start_page = int(input('请输入开始抓取数据的页码：'))
all_page = int(input('请输入结束抓取数据的页码：'))

file_down = open('在沪施工企业信用评价_'+str(start_page)+'.txt', 'a+', encoding='utf-8')
for page in range(start_page,all_page+1):
    head = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/80.0.3987.116 Safari/537.36",   # 用户代理
    }
    param = {
        'qyzjCode':'',
        'page':page,
        'qyNam':'',
    }
    search_url = 'https://ciac.zjw.sh.gov.cn/SHCreditInfoInterWeb/CreditBookAnounce/GetQyCreditReportAll'
    search_contect = requests.get(search_url,headers=head,params=param).text
    search_contect = "u'"+search_contect+"'"
    search_contect = eval(search_contect)
    search_contect = etree.HTML(search_contect)
    for i in range(1,11):
        data = search_contect.xpath('//html/body/table/tbody/tr['+str(i)+']/td/text()')
        file_down.write(str(data)+ '\n')
        print(str(data))
    file_down.write('【第'+str(page)+'页】\n')
    print('----------正在抓取第'+str(page)+'页-------------------  ')

