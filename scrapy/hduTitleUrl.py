# 爬取hdu：具体题目
import requests, time, threading, re
from urllib import request
from DBUtil import DBHelper
import time

Problem = []
Problem1 = []

proxy = {
    "https": "115.238.255.158-PPTP/",
    "https": "120.25.225.173-PPTP/",
    "https": "58.20.31.107-PPTP/",
    "https": "27.50.131.230-PPTP/",
}




db = DBHelper()
db.connectDatabase()

re1 = re.compile(r'<td align=center>(.*?)</td>', re.S)
re2 = re.compile(r'Total Submission\(s\): (\d+)', re.S)
re3 = re.compile(r'Accepted Submission\(s\): (\d+)', re.S)
re4 = re.compile(r'Problem Description.*?<div class=panel_content>(.*?)</div>', re.S)
re5 = re.compile(r'\SInput.*?<div class=panel_content>(.*?)</div>', re.S)
re6 = re.compile(r'\SOutput.*?<div class=panel_content>(.*?)</div>', re.S)
re7 = re.compile(r'<div style="font-family:Courier New,Courier,monospace;">(.*?)</div>', re.S)
re8 = re.compile(r'>Time Limit:.*?/(\d+) MS',re.S)
re9 = re.compile(r';Memory Limit:.*?/(\d+) K',re.S)
re10 = re.compile(r'<img.*?>')

def parse_page(url,problem):
    global Problem
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    response = requests.get(url, headers=headers,proxies=proxy)
    try:
        text = response.text
        td = re.findall(re1,text)[0]
        submission = re.search(re2, td)
        submission=submission.group(1)
        Accepted = re.search(re3, td)
        Accepted = Accepted.group(1)
        description = re.findall(re4, td)[0]
        description = re.sub(r'<i>|</i>|<br>|&quot','',description)
        description = re.sub(re10,'',description)
        Input = re.findall(re5, td)
        if len(Input)==0:
            Input = ''
        else:
            Input = Input[0]

        Input = re.sub(r'<i>|</i>|<br>|&quot', '', Input)
        Output = re.findall(re6, td)
        if len(Output)==0:
            Output = ''
        else:
            Output = Output[0]
        Output = re.sub(r'<i>|</i>|<br>|&quot', '', Output)
        putput = re.findall(re7, td)
        if len(putput)==1:
            SampleInput = ''
            SampleOutput = putput[0]
        elif len(putput)==0:
            SampleInput =''
            SampleOutput =''
        else:
            SampleInput = putput[0]
            SampleOutput = putput[1]
        SampleInput = re.sub(r'<i>|</i>|<br>|&quot', '', SampleInput)
        SampleOutput = re.sub(r'<i>|</i>|<br>|&quot', '', SampleOutput)
        time_limit = re.findall(re8, td)[0]
        mem_limit = re.findall(re9, td)[0]
        problem['submission']=int(submission)
        problem['Accepted']=int(Accepted)
        problem['description']=description
        problem['Input']=Input
        problem['Output']=Output
        problem['SampleInput']=SampleInput
        problem['SampleOutput']=SampleOutput
        problem['time_limit']=int(time_limit)
        problem['mem_limit']=int(mem_limit)

        sql = 'INSERT INTO probleminfo(pid,title,description,input,output,time_limit,mem_limit,sampleinput1,sampleoutput1,submission,acceptNum) VALUES ("%d","%s","%s","%s","%s","%d","%d","%s","%s","%d","%d")'
        db.cur.execute(sql % (problem['pid'], problem['title'], problem['description'], problem['Input'], problem['Output'], problem['time_limit'], problem['mem_limit'], problem['SampleInput'],problem['SampleOutput'], problem['submission'], problem['Accepted']))
        sql = 'update problem set flag = 1 where pid = %d' % problem['pid']
        db.cur.execute(sql)
    except Exception as e:  # 如果出错执行
        # 捕捉错误
        print(e)

    db.conn.commit()


def selectDB():
    sql = 'select pid,title,url from problem where flag = 0'
    rows=db.cur.execute(sql)
    info = db.cur.fetchall()
    for x in info:
        problem = {
            'title': x[1],
            'url': x[2],
            'pid': x[0]
        }
        Problem.append(problem)

# def insertDB():
#     for x in Problem1:
#         sql = 'INSERT INTO probleminfo(pid,title,description,input,output,time_limit,mem_limit,sampleinput1,sampleoutput1,submission,acceptNum) VALUES ("%d","%s","%s","%s","%s","%d","%d","%s","%s","%d","%d")'
#         db.cur.execute(sql % (x['pid'],x['title'],x['description'],x['Input'],x['Output'],x['time_limit'],x['mem_limit'],x['SampleInput'],x['SampleOutput'],x['submission'],x['Accepted']))
#     db.conn.commit()



def main():
    num = 0
    for x in Problem:
        parse_page(x['url'], x)
        print(num)
        num += 1
        # time.sleep(3)


if __name__ == '__main__':
    # for i in range(4):
    # res = requests.get('http://httpbin.org/get',proxies=proxy)
    # print(res.text)
    selectDB()
    main()
    db.close()
