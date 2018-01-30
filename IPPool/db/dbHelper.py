#coding=utf-8
from pymongo import MongoClient,UpdateOne
from gevent import monkey
monkey.patch_all()
from IPPool.config import HOST,POST,DBName,FALSE_NUM


class DBHelper:
    def __init__(self,collection):
        self.client = MongoClient(HOST,POST,socketTimeoutMS=10000,connectTimeoutMS=10000)
        self.db = self.client[DBName]
        self.collection = self.db[collection]
    def count(self):
        return self.collection.count()
    def find(self):
        return self.collection.find()
    def select(self,count=10):
        num = self.collection.count()
        if count<num:
            data = self.collection.find({},{'IpAddress':1,'ip':1,'port':1,'_id':0}).sort([('rate',-1),('aveVisitTime',1),('lastVisitTime',1)]).limit(count)
            result = []
            for item in data:
                result.append(item)
            return result
        else:
            data = self.collection.find({},{'IpAddress':1,'ip':1,'port':1,'_id':0}).sort([('rate',-1),('aveVisitTime',1),('lastVisitTime',1)])
            result = []
            for item in data:
                result.append(item)
            return result
    def insert(self,value):
        try:
            self.collection.insert(value)
        except Exception:
            pass
    def delete(self,condition=FALSE_NUM):
        self.collection.remove(condition)

    def update(self,data):
        try:
          requests = []
          for item in data:
              ip = item[0]
              condition = item[1]
              requests.append( UpdateOne({'_id':ip['_id']},{"$set":condition}))
          self.collection.bulk_write(requests)
        except Exception as e:
            print e.message
    def close(self):
        self.client.close()


if __name__=='__main__':
    dbHelper = DBHelper('ip')
    print dbHelper.select(1)
    # for item in a.select():
    #     print item