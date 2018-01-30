#coding=utf-8
from IPPool.db.dbHelper import DBHelper
import time

def store_data(queue,collectionName):
    time.sleep(5)
    BATCH = 100
    rows = []
    dbHelper = DBHelper(collectionName)
    while True:
        if queue.qsize()!=0:
            row = queue.get()
            rows.append(row)
            if len(rows) == BATCH:
                dbHelper.insert(rows)
                rows = []
        else:
            time.sleep(5)
            if queue.qsize()!=0:
                continue
            elif rows:
                print 'last', len(rows)
                dbHelper.insert(rows)
                dbHelper.close()
            break

