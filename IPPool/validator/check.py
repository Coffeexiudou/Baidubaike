#coding=utf-8
from validator import check_ip
from IPPool.db.dbHelper import DBHelper
from multiprocessing import Process,Queue
from gevent import monkey; monkey.patch_all()
from IPPool.config import PROCESS_NUM,CONST_TIME
import gevent
import time
"""
todo:去重
"""
class Check(object):
    def __init__(self,collectionName):
        self.collection = collectionName

    def start_check(self):
        dbHelper = DBHelper(self.collection)
        data = dbHelper.find()
        pList = []
        data = list(data)
        dbHelper.close()
        q = Queue()
        ave = len(data) / (PROCESS_NUM - 1)
        for i in xrange(PROCESS_NUM):
            a, b = i * ave - 1 if i * ave - 1 > 0 else 0, (i + 1) * ave - 1 if (i + 1) * ave < len(data) else len(data)
            p = Process(target=self.__check_ipList, args=(data[a:b],q,))
            pList.append(p)
            p.start()
        updatep = Process(target=self.__update,args=(q,))
        updatep.start()
        updatep.join()
        for p in pList:
            p.join()

    def __check_ipList(self,ipList,q):
        tasks = []
        for ip in ipList:
            tasks.append(gevent.spawn(self.__check, ip,q, ))
        gevent.joinall(tasks)

    def __check(self,ip,q):
        flag = check_ip(ip['IpAddress'])
        updatedata = []
        if flag:
            checkNum = ip['checkNum'] + 1
            lastVisitTime = flag
            aveVisitTime = (flag + ip['aveVisitTime']) / checkNum
            rate = ((float(checkNum)+1)/(ip['falseNum']+1))*(checkNum-ip['falseNum'])
            condition = {'checkNum': checkNum, 'lastVisitTime': lastVisitTime, 'aveVisitTime': aveVisitTime,'rate':rate}
            updatedata.append(ip)
            updatedata.append(condition)
            q.put(updatedata)
        else:
            falseNum = ip['falseNum'] + 1
            checkNum = ip['checkNum'] + 1
            lastVisitTime = float('inf')
            aveVisitTime = (CONST_TIME + ip['aveVisitTime']) / float(checkNum)
            rate = ((float(checkNum)+1)/(falseNum+1))*(checkNum-falseNum)
            condition = {'checkNum': checkNum, 'falseNum': falseNum, 'aveVisitTime': aveVisitTime,
                         'lastVisitTime': lastVisitTime,'rate':rate}
            updatedata.append(ip)
            updatedata.append(condition)
            q.put(updatedata)

    def __update(self,q):
        time.sleep(5)
        BATCH = 200
        rows = []
        dbHelper = DBHelper(self.collection)
        while True:
            if q.qsize() != 0:
                row = q.get()
                rows.append(row)
                if len(rows) == BATCH:
                    dbHelper.update(rows)
                    rows = []
            else:
                time.sleep(5)
                if q.qsize() != 0:
                    continue
                elif rows:
                    print 'update', len(rows)
                    dbHelper.update(rows)

                break
      #  dbHelper.delete()
        dbHelper.close()


if __name__ == '__main__':
    a = Check('ip')
    import time
    start = time.time()
    a.start_check()
    print time.time()-start