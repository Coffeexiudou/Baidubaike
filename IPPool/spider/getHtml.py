# coding=utf-8
import requests
from IPPool import config
import chardet
from IPPool.db.dbHelper import DBHelper

class HtmlDownload(object):
    @staticmethod
    def download(url):
        try:
            session = requests.Session()
            session.trust_env = False
            res = session.get(url, headers=config.get_header(),timeout=config.TIME_OUT)
            res.encoding = chardet.detect(res.content)['encoding']
            if (not res.ok) or len(res.content) < 500:
                raise ConnectError
            else:
                return res.text
        except Exception:
            count = 0
            while count < config.RETRY_TIME:
                try:
                    dbHelper = DBHelper('ip')
                    proxy = dbHelper.select(1)
                    ip = proxy[0]['IpAddress']
                    proxies = {"http": "http://{ip}".format(ip=ip), "https": "http://{ip}".format(ip=ip)}
                    dbHelper.close()
                    res = session.get(url=url, headers=config.get_header(),proxies=proxies,timeout=config.TIME_OUT)
                    res.encoding = chardet.detect(res.content)['encoding']
                    if (not res.ok) or len(res.content) < 500:
                        raise ConnectError
                    else:
                        return res.text
                except Exception:
                    count += 1
        return None


if __name__ == '__main__':
    print HtmlDownload.download('https://www.baidu.com')

