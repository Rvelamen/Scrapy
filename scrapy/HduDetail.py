# 爬取hdu：Title,pid,url
import requests, time, threading, re
from urllib import request
from DBUtil import DBHelper

Problem = []

def parse_page(url):
    global Problem
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    text = response.text
    request.urlretrieve(url,'html/1.html')
    reTable = re.compile(r'<table.*?>(.*?)</table>', re.S)
    reScript = re.compile(r'<script language="javascript">(.*?)</script>', re.S)
    reP = re.compile(r'p\(.*?"(.*?)",.*?\);',re.S)
    rePid = re.compile(r'p\(\d,(\d{4}).*?\);',re.S)

    tbody = re.findall(reTable, text)[2]
    Scriptx = re.findall(reScript, tbody)[0]
    title = re.findall(reP, Scriptx)

    pid = re.findall(rePid,Scriptx)
    for x, y in zip(title, pid):
        z = x.strip('\\"')
        problem = {
            'title': z,
            'url': 'http://acm.hdu.edu.cn/showproblem.php?pid=%d'%int(y),
            'pid': int(y)
        }
        Problem.append(problem)

def insertDB():
    db = DBHelper()
    db.connectDatabase()
    for x in Problem:
        sql = 'INSERT INTO problem (pid,title,url) VALUES ("%d","%s","%s")'
        db.cur.execute(sql % (x['pid'],x['title'],x['url']))
    db.conn.commit()
    db.close()


def main():
    for x in range(55, 56):
        url = 'http://acm.hdu.edu.cn/listproblem.php?vol=%d' % x
        parse_page(url)


if __name__ == '__main__':
    main()
    insertDB()