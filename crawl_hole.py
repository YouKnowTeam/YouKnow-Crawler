# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 19:11:46 2018

"""

import requests
import time
import pymysql

db = pymysql.connect(host = 'localhost', port = 3306, user = 'group3', passwd = 'group3', db = 'group3', charset='utf8')

cursor = db.cursor()

url = 'http://www.pkuhelper.com:10301/pkuhelper/../services/pkuhole/api.php'
param = {
          'action' : 'getlist',
          'p' : 1
          }
p_id = 0
updatetime = 60

while True:  
    r = requests.get(url, params = param)
    r_js = r.json()
    datalist = r_js['data']
    for i in range(len(datalist)):
        j = len(datalist) - i - 1
        if int(datalist[j]['pid']) > p_id:
            p_id = int(datalist[j]['pid'])
            det = datalist[j]['text']
            det.encode("utf-8")
            bri = det[:10]
            bri.encode("utf-8")
#            print(det)
#            print('\n')
            sql = """INSERT INTO Msg(SrcID, Brief, Detail) VALUES ('%s', '%s', '%s')""" % ('PKU tree hole', bri, det)
            
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
#        else:
#            print('No update')
    time.sleep(updatetime);

#db.close()