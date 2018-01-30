#coding=utf-8
from IPPool.spider.crawl import start_crawl
from IPPool.validator.check import Check
from IPPool.db.dbHelper import DBHelper
from IPPool.config import IP_NUM
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig()
"""

定时检查db　———— 调用check ————　如果可用ip数量少于某值　———— 启动爬虫

"""



def start(collection):
    # dbHelper = DBHelper(collection)
    # if dbHelper.count()<IP_NUM:
    #     dbHelper.close()
   # while(True):
    start_crawl(collection)
    # dbHelper.close()
    Check(collection).start_check()
   # time.sleep(60*2)

def delete(collection):
    dbHelper = DBHelper(collection)
    dbHelper.delete()
    dbHelper.close()


if __name__=='__main__':
    sched = BlockingScheduler()
    sched.add_job(start,'interval',minutes=30,args=['ip'])
    sched.add_job(delete,'interval',hours=2,args=['ip'])
    sched.start()
  #start('ip')
    # import matplotlib.pyplot as plt
    # import numpy as np　
    # from mpl_toolkits.mplot3d import Axes3D
    # x = range(1,100)
    # y = list()
    # for i in x:
    #     y.append(i+np.random.randint(0,100))
    # x = np.array(x)
    # y = np.array(y)
    # z = (y/x)*(y-x)
    # print x
    # print y
    # print z
    # ax = plt.subplot(111,projection='3d')
    # ax.scatter(x,y,z)
    # ax.set_zlabel('z')
    # ax.set_ylabel('y')
    # ax.set_xlabel('x')
    # plt.show()