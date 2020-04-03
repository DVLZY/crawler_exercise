# coding=utf-8
# python 3.8.2
# pycharm

import requests
import time
import parsel  # parsel 数据解析模块

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

# 获取最后一页的页码
def last_page():
    base_url = 'https://www.kuaidaili.com/free/inha/'
    base_rst = parsel.Selector(requests.get(base_url, headers=head).text)
    last_page = base_rst.xpath('//*[@id="listnav"]/ul/li[9]/a/text()').extract_first()  # 获取最后一页的页码
    return last_page

# 检测IP质量，如果响应时间大于0.1秒就报错
def check_ip(proxies_list):
    can_use = []
    for proxy in proxies_list:
        try:
            rst = requests.get('https://www.baidu.com', headers=head, proxies=proxy, timeout=0.1)
            if rst.status_code == 200:
                can_use.append(proxy)
                # file_down.write(str(proxy) + '\n')  #写入文件
        except Exception as err:
            print('当前IP\t【超时】\t{}'.format(proxy))
        finally:
            print('当前IP\t检测通过\t{}'.format(proxy))
    print()
    return can_use
file_down = open('IP代理池_' + time.strftime("%Y-%m-%d %H-%M-%S") + '.txt', 'a+', encoding='utf-8')    #创建文件
proxies_list = []
last_page = last_page()
time.sleep(1)
# 遍历所有页面
for page in range(0, int(last_page)):
    page = page + 1
    print('正在获取第{}页数据'.format(page))
    url = 'https://www.kuaidaili.com/free/inha/{}'.format(str(page))
    rst = requests.get(url, headers=head).text
    rst = parsel.Selector(rst)  # 转换数据类型,把text转换成html，这样可以被xpath定位
    html_list = rst.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')  # xpath利用父节点获取信息（另一种定位思路）
    # 遍历所有IP条目
    for tr in html_list:
        proxies_dict = {}
        http_type = tr.xpath('./td[4]/text()').extract_first()
        ip_num = tr.xpath('./td[1]/text()').extract_first()
        ip_port = tr.xpath('./td[2]/text()').extract_first()
        proxies_dict[http_type] = ip_num + ':' + ip_port
        file_down.write(str(proxies_dict) + '\n')  # 写入文件
        print(proxies_dict)
        proxies_list.append(proxies_dict)
    time.sleep(1)
    print()

can_use = check_ip(proxies_list)
print('IP数量为：', len(proxies_list))
print('能用的代理IP数量为', len(can_use))
