import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import random
import sqlite3
#这个是第一个爬虫
USER_AGENTS = [
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
        ]

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'Hm_lvt_022c6fcfbc81400674cdf480300687b5=1587629570; BAIDUID=526D6E959C18E36E6E507F5009F748B6:FG=1; Hm_lpvt_022c6fcfbc81400674cdf480300687b5=1587706045',
    'Host': 'dianying.nuomi.com',
    'Origin': 'http://dianying.nuomi.com',
    'Referer': 'http://dianying.nuomi.com/movie/boxoffice',
    'User-Agent': random.choice(USER_AGENTS),
    'X-Requested-With': 'XMLHttpRequest'
    }

#测试使用 会先删掉已有db文件里的table
try:
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute("DROP TABLE MOVIESALE;")
    conn.commit()
    conn.close()
except:
    pass
#定义table
conn = sqlite3.connect('movie.db')
c = conn.cursor()
c.execute('''CREATE TABLE MOVIESALE
(ID INT  NOT NULL,
DATE TEXT NOT NULL,
NAME TEXT NOT NULL,
TOTALDAYS TEXT NOT NULL,
TOTALBOX INT NOT NULL,
REALTIMEBOX TEXT NOT NULL,
BOXPERCENTAGE REAL NOT NULL,
SCHEDULEPERCENTAGE REAL NOT NULL,
SEATPERCENTAGE REAL NOT NULL,
SEATSCHEDULEPERCENTAGE REAL NOT NULL,
SHOW TEXT NOT NULL,
PERSONTIME INT NOT NULL,
AVERAGEPERSONTIME INTEGER NOT NULL,
AVERAGEINCOME INTEGER NOT NULL,
AVERAGETICKETPRICE INTEGER NOT NULL,
PRIMARY KEY (ID,DATE));''')
conn.commit()
conn.close()
#爬取数据
url = 'http://dianying.nuomi.com/movie/boxrefresh'
#用pandas更改日期
dates  = pd.DataFrame({'date':pd.date_range(start = '2018-01-01',end = '2018-12-31',freq = 'D')})
dates['date'] = dates['date'].astype('str')
finallist= []
for i in dates['date']:
    print(i)
    #动态网页 模拟post
    data={'isAjax':'true','date':i}
    req = requests.post(url,data=data,headers=headers)
    str_data = req.content
    str_data = json.loads(str_data)
    for item in str_data['real']['data']['detail']:

        databaselist = []
        databaselist.append(item['movieId'])
        databaselist.append(i)
        databaselist.append(item['movieName'])
        list= []
        list.append(i)
        list.append(item['movieName'])
        for j in range(1,13):
            value = item['attribute'][str(j)]['attrValue']
            if j == 2 or j == 9:
                if type(value) == int or type(value) == float:
                    pass
                #str数据变成float
                elif value.isdigit():
                    value = float(value)
                elif value[-1] == '万':
                    value = float(value[0:-1])*10000.0
                elif value[-1] == '亿':
                    value = float(value[0:-1])*100000000.0
            databaselist.append(value)
            if j == 1 or j ==2:
                continue
            items = item['attribute'][str(j)]
            list.append(items['attrValue'])
        print(databaselist)
        date = i
        finallist.append(list)

        conn = sqlite3.connect('movie.db')
        c = conn.cursor()
        print(databaselist[0],databaselist[1])
        #insert into database
        c.execute(
            '''
            INSERT INTO MOVIESALE (ID,DATE,NAME,TOTALDAYS,TOTALBOX,REALTIMEBOX,BOXPERCENTAGE,SCHEDULEPERCENTAGE,SEATPERCENTAGE,SEATSCHEDULEPERCENTAGE,SHOW,PERSONTIME,AVERAGEPERSONTIME,AVERAGEINCOME,AVERAGETICKETPRICE)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
            ''',(databaselist[0],databaselist[1],databaselist[2],databaselist[3],databaselist[4],databaselist[5],databaselist[6],databaselist[7],databaselist[8],databaselist[9],databaselist[10],databaselist[11],databaselist[12],databaselist[13],databaselist[14])
        )
        conn.commit()
        conn.close()
#输出csv
result = pd.DataFrame(finallist,columns = {'日期':'','片名':'','实时票房':'','票房占比':'','排片占比':'','上座率':'','排座占比':'','场次':'','人次':'','场均人次':'','场均收入':'','平均票价':''})
result.to_csv('result.csv')


