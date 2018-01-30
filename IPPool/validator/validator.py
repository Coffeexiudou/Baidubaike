#coding=utf-8
import requests
from IPPool.config import get_header,TEST_URL,TIME_OUT
import time

def check_ip(proxy):
    session = requests.Session()
    session.trust_env = False
    proxies = {
        "http": "http://"+proxy,
        "https": "https://"+proxy
    }

    try:
        startTime = time.time()
        res = session.get(TEST_URL,headers=get_header(),proxies=proxies,timeout=(1,3))
        if (not res.ok) or len(res.content) < 500:
            return False
        else:
            visitTime = time.time()-startTime
         #   print visitTime
            return visitTime
    except Exception :
       # print 'false'
        return False
if __name__=='__main__':
    ip = '120.26.14.14:3128'
    check_ip(ip)
    # from gevent import monkey;
    #
    # monkey.patch_all(thread=False, select=False)
    # import gevent
    # from IPPool.db.dbHelper import DBHelper
    #
    # dbHelper1 = DBHelper('ip')
    # data = dbHelper1.select(50)
    # for item in data:
    #     flag = check_ip(item['IpAddress'])
    #   #  print flag
    #     if flag:
    #         print 'success'
   # check_ip(ip)
