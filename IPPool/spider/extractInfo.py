# coding=utf-8
import sys
from lxml import etree


def Extract_Info(html, parser):
    root = etree.HTML(html)
    proxies = root.xpath(parser['pattern'])
    proxyList = []
    for proxy in proxies:
        try:
            data = dict()
            ip = proxy.xpath(parser['position']['ip'])[0].text
            port = proxy.xpath(parser['position']['port'])[0].text
            data['ip'] = ip
            data['port'] = port
            data['IpAddress'] = ip + ':' + port
            data['checkNum'] = 0
            data['falseNum'] = 0
            data['lastVisitTime'] = 0
            data['aveVisitTime'] = 0
            data['rate'] = 0
            proxyList.append(data)
        except Exception:
            continue
    return proxyList


if __name__ == '__main__':
    pass