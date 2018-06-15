# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 00:18:48 2018

@author: LIUCHIZHOU
"""

import urllib2
from bs4 import BeautifulSoup
import time
import re
import pymysql

import sys #要重新载入sys。因为 Python 初始化后会删除 sys.setdefaultencoding 这个方 法
reload(sys) 
sys.setdefaultencoding('utf-8')

db = pymysql.connect(host = 'localhost', port = 3306, user = 'group3', passwd = 'group3', db = 'group3', charset='utf8')
cursor = db.cursor()

url = "http://www.dean.pku.edu.cn/web/notice.php"
url_detail = "http://www.dean.pku.edu.cn/web/"

p_id = 0
updatetime = 60

while True:  
    page = urllib2.Request(url)  
    page_info = urllib2.urlopen(page).read()#.decode('utf-8')
    soup = BeautifulSoup(page_info, 'html.parser')
    data = soup.find_all(class_="active")[2:-1]

    for i in range(len(data)):
        j = len(data) - i - 1
        id_ = data[j]["href"].split('=')[1]
        
        if int(id_) > p_id:
            new_url = url_detail + data[j]["href"]
            bri = data[j].string
            detail_page = urllib2.Request(new_url)
            detail_page_info = urllib2.urlopen(detail_page).read()#.decode('utf-8')
            detailsoup = BeautifulSoup(detail_page_info, 'html.parser')
            data_detail = detailsoup.find(class_="newsinfo_box")
            det = re.sub('<[^>]*>', '', str(data_detail))
            print id_
            p_id = int(id_)
            sql = """INSERT INTO Msg(SrcID, Brief, Detail) VALUES ('%s', '%s', '%s')""" % ('PKU dean', bri, det)
            
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        #else:
        #    print("no update")
    
    time.sleep(updatetime);

db.close()
