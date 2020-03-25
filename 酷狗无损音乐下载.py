# -*- coding : 'UTF-8' -*-
#  Author:XSX
# Python3.8 Pycharm
# https://www.52pojie.cn/thread-1140730-1-1.html 原帖链接
# todo(lin) 加一个用户代理池
# todo(lin) 实现自动重命名
import requests
from urllib import parse
from GetRandomheader import Randomheader
import re
import json
import time

def URLDecode(text):
    Decode = parse.quote(text)
    print('正在查找【{}】的无损音乐------请等待'.format(text))
    return Decode

def GetitemInfo(Decodetext, headers):
    ItemInfos = []
    url1 = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery1124047909927884881864_1584769239146&keyword={}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1584769239150'.format(Decodetext)
    r = requests.get(url1, headers=headers)
    r.encoding = r.apparent_encoding
    JsonText = json.loads(r.text[43:-2])
    for i in JsonText["data"]["lists"]:
        contents = {}
        contents['SongName'] = i['SongName']
        contents['AlbumID'] = i['AlbumID']
        contents['FileHash'] = i['FileHash']
        contents['SQFileHash'] = i['SQFileHash']
        contents['HQFileHash'] = i['HQFileHash']
        contents['MvHash'] = i['MvHash']
        ItemInfos.append(contents)
    return ItemInfos

def GetDownLinks(ItemInfos, headers):
    try:
        DownLists = []
        for Iteminfo in ItemInfos:
            ID = Iteminfo['AlbumID']
            Hash = Iteminfo['SQFileHash']
            downurl = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191006287980471670584_1584780452839&hash={0}&album_id={1}&dfid=3dTk9E0IfcV50gyRKr3OGZey&mid=0407f15d60c01b0ccb16bf2323d904b2&platid=4&_=1584780452841'.format(Hash, ID)
            time.sleep(3)
            r1 = requests.get(downurl, headers=headers)
            r1.encoding = r1.apparent_encoding
            DownLists.append(r1.text[42:-2].replace('\\', '').encode('utf8').decode('unicode_escape'))
        print('正在解析无损音质歌曲' + '\n' + '==========================' + '\n' + '说明：解析后无下载地址是因为该歌曲没有无损音质或需要付费下载' + '\n' + '==========================' + '>>>>>>>请稍后<<<<<<<')
        return DownLists
    except:
        pass

def GetSongLinks(DownLists):
    try:
        n = 0
        for DownList in DownLists:
            link = re.findall(r'.*' + '"play_url":"' + '(.*)' + '","authors"', str(DownList))
            n += 1
            print('正在解析第【{}】首无损音乐地址！'.format(n) + '\n' + '请点击下方链接下载保存音乐>>>>>>>>')
            print(link)
    except:
        pass

if __name__ == '__main__':
    head = Randomheader()
    GetSongLinks(GetDownLinks(GetitemInfo(URLDecode(input('请输入需要搜索的歌曲名称：')), head), head))