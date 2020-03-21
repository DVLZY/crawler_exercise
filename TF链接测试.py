##
import urllib.request
import random
import re
from lxml import etree


uapools = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    ]
def UA():
    #利用自定义函数UA实现随机使用浏览器标识
    opener = urllib.request.build_opener()
    randomUA = random.choice(uapools)
    # 从用户代理池中随机选取一个标识
    UserAgent = ('User-Agent',randomUA)
    opener.addheaders=[UserAgent]
    urllib.request.install_opener(opener)
    # 将opener对象代表的浏览器标识安装到全局

print()
file = input('请输入要测试的文件所在路径:')
data = open(file,encoding='utf-8').read()
name_url_list= re.compile('testflight.apple.com/join/(\w{8})',re.S).findall(data)
file_down = open(r'./TestFlight测试结果.txt', 'a+', encoding='utf-8')

for i in name_url_list:
    UA()
    url = "https://testflight.apple.com/join/"+i
    data = urllib.request.urlopen(url).read().decode('utf-8','ignore')
    html = etree.HTML(data)
    try:
        name = re.compile(' <title>Join the (.*?) beta - TestFlight - Apple</title>').findall(data)[0]
    except Exception as err:
        name = ''
        pass
    try:
        a = html.xpath('//*[@id="main"]/section/div/div/div/div[2]/span/text()')[0]
    except Exception as err:
        a = html.xpath('//*[@id="main"]/section/div/div/div/div[1]/div[2]/h2/span/text()')[0]
        pass
    file_down.write('【'+url+'】 【'+name+"】 【"+a+"】"+ '\n')
    print('【'+url+'】 【'+name+"】 【"+a+"】")

