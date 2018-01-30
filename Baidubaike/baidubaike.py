#coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
from IPPool import config
from IPPool.db.dbHelper import DBHelper


CLASS_DISAMBIGUATION = ['lemmaWgt-subLemmaListTitle']
CLASS_SUMMARY = ['lemma-summary']
CLASS_BASICINFO = ['basic-info cmn-clearfix']

class Baidubaike:
    def __init__(self,item):
        self.item = item
        self.url = 'https://baike.baidu.com/item/'+item
        self.pattern1 = re.compile(u'^收起$')
        self.pattern2 = re.compile(r'\[\d+\]|\[\d+\-\d+\]')
        self.data = dict()
        self.data['item'] = item

    def get_content(self):
        try:
            self.__get_page()
            if self.data['status'] != 200:
                return self.data
            else:
                return self.__extract_info()
        except Exception,e:
            raise ValueError(e.message)

    def __extract_info(self):
        summary = self.soup.find('div', class_=CLASS_SUMMARY).get_text().strip()
        summary = self.pattern2.sub('', summary)
        self.data['basicInfo'] = []
        try:
            basicInfo = self.soup.find('div', class_=CLASS_BASICINFO)
            for item in basicInfo.find_all('dl'):
                for dt,dd in zip(item.find_all('dt'),item.find_all('dd')):
                    info = dict()
                    key = dt.get_text().strip().encode('utf-8')
                    vals = dd.get_text().strip().replace('\n',' ').split(' ')
                    value = ''
                    for val in vals:
                        value =value+self.pattern1.sub('',val)+' '
                    info[key] = value.strip().encode('utf-8')
                    self.data['basicInfo'].append(info)

        except:
            self.data['basicInfo'] = []
        tags = []
        try:
            tag = self.soup.find('dd', id='open-tag-item')
            val = ''
            for item in tag.find_all('span'):
                val += item.string.strip().encode('utf-8') + ' '
           # tags = tag.get_text().replace('\n', '').split(u'，')
            self.data['tag'] = val.strip()
        except:
            self.data['tag'] = tags
        self.data['summary'] = summary.encode('utf-8')
        return self.data

    def __connect(self):
        try:
            self.session = requests.Session()
            self.session.trust_env = False
            self.headers = config.get_header()
            self.res = self.session.get(self.url, headers=self.headers)
            self.res.encoding='utf-8'
        except Exception:
            count = 0
            while count < config.RETRY_TIME:
                try:
                    dbhelper = DBHelper('ip')
                    proxy = dbhelper.select(1)
                    ip = proxy[0]['IpAddress']
                    proxies = {"http": "http://{ip}".format(ip=ip), "https": "http://{ip}".format(ip=ip)}
                    dbhelper.close()
                    self.res = self.session.get(url=self.url, headers=config.get_header(), proxies=proxies,
                                                timeout=config.TIME_OUT)
                    self.res.encoding = 'utf-8'
                except Exception as e:
                    print e.message

    def __get_page(self):
        self.__connect()
        self.page = self.res.text.replace('&nbsp;', '')
        self.soup = BeautifulSoup(self.page, 'lxml')
        if '页面不存在' in self.res.content:
            self.data['status'] = 202
           # raise ValueError(u'页面不存在')
        elif self.soup.find(id='vf'):
            self.data['status'] = 203
       #     raise ValueError(u'请求过快')
        elif self.soup.find(class_=CLASS_DISAMBIGUATION):
            self.data['status'] = 201
       #     raise ValueError(u'多义词')
        else:
            self.data['status'] = 200


if __name__ == '__main__':
    test = Baidubaike(u'乔丹')
    print test.get_content()