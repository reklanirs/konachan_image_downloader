#!/usr/bin/python2.7
# -*- coding: utf-8 -*- import requests
import os
import re
import sys
import math
import requests
import time
import json
import lxml
import demjson
from random import choice
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from lxml import etree
from os.path import join, getsize
reload(sys)
#sys.stdout=open('out.txt','w')
log = open('log.txt','a')
links = open('links.txt','a+')
fsus = open('sus.txt','a+')
ffai = open('fail.txt','a+')
links.seek(0,0)
fsus.seek(0,0)
ffai.seek(0,0)

url = 'http://konachan.com/post?tags=yahari_ore_no_seishun_love_come_wa_machigatteiru.'
recaplink = True

keyword = url[ url.find('tags=') + 5 :]
# keyword = 'yahari_ore_no_seishun_lovecome_wa_machigatteiru.+'
maxpage = 1
needpage = -1  #only download first ${needpage} pages, -1 for all.
id_link = {}
succes_id_link = {}
failed_id_link = {}
download = True
wait_time = 1


def writeln(s):
    print s
    log.write(s + '\n')
    log.flush()
    pass

def deal_one_page(x):
    r = requests.get(url + '&page=%d'%x)
    s = r.text.encode('utf-8')
    #links.write(s)

    soup = BeautifulSoup(s,'lxml')
    l = soup.find_all(id='post-list-posts')[0]
    li = l.find_all('li')
    for i in li:
        a = i.find_all('a')
        id_link[i['id'][1:]] = a[1]['href']
    pass

def dealId(picid, rawurl):
    pngurl = rawurl[rawurl.find('.com')+5:]
    pngurl = 'http://konachan.com/image/' + pngurl[pngurl.find('/')+1:]
    pngurl = pngurl[:-3] + 'png'
    r = requests.get(pngurl)
    name = ''
    if len(r.content) < 10240:
        r = requests.get(pngurl[:-3] + 'jpg')
        if len(r.content) < 10240:
            return -1
        else:
            name = picid + '.jpg'
    else:
        name = picid + '.png'
    with open(name, "wb") as code:
        code.write(r.content)
    if name[-3:] == 'jpg':
        return 0
    elif name[-3:] == 'png':
        return 1
    else:
        return -1
    pass


def main():
    global maxpage,needpage,keyword

    while True:
        i = fsus.readline()
        j = fsus.readline()
        if len(j)==0:
            break
        succes_id_link[i[:-1]] = j[:-1]
    while True:
        i = ffai.readline()
        j = ffai.readline()
        if len(j)==0:
            break
        failed_id_link[i[:-1]] = j[:-1]

    sys.stdin = open('links.txt','r')
    while not recaplink:
        try:
            i = raw_input().strip()
            j = raw_input().strip()
            if len(i)>=1 and i[0]=='p':
                i = i[1:]
            id_link[i] = j
            pass
        except Exception, e:
            break

    if recaplink:
        writeln('Begin capturing the main page.')
        # payload = {'tags':keyword}
        # r = requests.get(url, data = payload)
        r = requests.get(url)
        s = r.text.encode('utf-8')
        #links.write(s)
        l = re.findall('page=.*&',s)
        for i in l:
            tmp = int(i[i.find('=')+1:i.find('&')])
            if tmp>maxpage:
                maxpage = tmp
        #print maxpage
        writeln('There are at most %d pages to download then.'%(maxpage))
        r = maxpage
        if needpage!=-1:
            r = min(needpage,maxpage)
        pre = 0
        for i in range(1,r + 1):
            deal_one_page(i)
            print 'page %3d finished. Added %2d pictures.'%(i,len(id_link) - pre)
            pre = len(id_link)
            time.sleep(wait_time)
        writeln('.\n.\nPicture links capture finished.')

        linkout = open('links.txt','w')
        for i,j in id_link.items():
            linkout.write(i + '\n' + j + '\n')
        linkout.flush()
        linkout.close()


    if download:
        #stdout=open('log.txt','w')
        fsus.seek(0, os.SEEK_CUR)
        ffai.seek(0, os.SEEK_CUR)
        if not os.path.exists(keyword):
            os.mkdir(keyword)
        os.chdir(keyword)
        loc = os.getcwd()
        tmp = 'Start downloading %d pictures. Save path is %s.'%(len(id_link),loc)
        writeln(tmp)

        sus = 0
        fail = 0
        for i,j in id_link.items():
            if i in succes_id_link:
                sus += 1
                writeln('The pic %7s downloaded before,ignore.\tNow sus:%5d,fail:%5d.'%(i,sus,fail))
                continue
            tmp = dealId(i, j)
            if tmp >= 0:
                sus += 1
                succes_id_link[i] = j
                print i,j
                fsus.write(i + '\n' + j + '\n')
                fsus.flush()
                if i in failed_id_link:
                    del failed_id_link[i]
                sufix = ''
                if tmp==0:
                    sufix = '.jpg'
                else:
                    sufix = '.png'
                writeln('The pic %7s%s download successed.\tNow sus:%5d,fail:%5d.'%(i,sufix,sus,fail))
            else:
                fail += 1
                failed_id_link[i] = j
                ffai.write(i + '\n' + j + '\n')
                ffai.flush()
                writeln('The pic %7s download failed.       \tNow sus:%5d,fail:%5d.'%(i,sus,fail))
            time.sleep(wait_time)
        writeln( '.\n.\nAll Download Finisned.\nsus:%5d,fail:%5d.'%(sus,fail) )
    writeln('.\n.\nFin.\n')
    pass



if __name__ == '__main__':
	main()
