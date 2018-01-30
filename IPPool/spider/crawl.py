# coding=utf-8
from IPPool.config import parseList
from multiprocessing import Process, Queue
import threading
from getHtml import HtmlDownload
from extractInfo import Extract_Info
from IPPool.db.dataStore import store_data
from multiprocessing import Process
from gevent import monkey; monkey.patch_all()
import gevent
"""
爬　————　验证　————　存　
"""
class Crawl(object):
    proxies = set()

    def __init__(self,queue):
        self.q = queue
    def __extract_info(self,url,parser):
        html = HtmlDownload.download(url)
        if html is not None:
            proxyList = Extract_Info(html, parser)
            for proxy in proxyList:
                if proxy['IpAddress'] not in self.proxies:
                    self.proxies.add(proxy['IpAddress'])
                    self.q.put(proxy)
    def __extract(self,parser):
        tasks = []
        for url in parser['urls']:
            tasks.append(gevent.spawn(self.__extract_info, url,parser, ))
        gevent.joinall(tasks)
    def run(self):
        self.pList = []
        for parser in parseList:
            p = Process(target=self.__extract,args=(parser,))
            self.pList.append(p)
            p.start()
    def finish(self):
        for p in self.pList:
            p.join()

def start_crawl(collection):
    q = Queue()
    a = Crawl(q)
    a.run()
    p1 = Process(target=store_data, args=(q,collection,))
    p1.start()
    p1.join()
    a.finish()
if __name__ == '__main__':
    import time
    start = time.time()
    start_crawl('ip')
    print time.time()-start