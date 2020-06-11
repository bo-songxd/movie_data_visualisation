
#因为1。py需要爬的时间很久 ， 后面的网站有需要其中的数据， 这个程序读取moviesale的id 之后根据id爬 info
import requests
from bs4 import BeautifulSoup
import json
import random
import sqlite3
try:
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute("DROP TABLE MOVIEINFO;")
    conn.commit()
    conn.close()
except:
    pass
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
conn = sqlite3.connect('movie.db')
c = conn.cursor()
c.execute('''CREATE TABLE MOVIEINFO
(ID INT NOT NULL,
DIRECTOR TEXT,
ACTOR TEXT,
AREA TEXT,
TIME INT,
PRIMARY KEY (ID));
''')
conn.commit()

c.execute("SELECT ID from MOVIESALE")
idcollection = c.fetchall()
print(len(idcollection))
idrepeat = []
for row in idcollection:
    id = row[0]
    if id in idrepeat:
        continue
    print(id)
    idrepeat.append(id)
    url = 'https://dianying.nuomi.com/movie/detail?movieId=' + str(id)
    print(url)
    strhtml = requests.get(url, headers=headers)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data = soup.find('div', attrs={'class': "info"})
    title = data.find('h4').string
    if title == None:
        continue
    info = data.find('div', attrs={'class': 'content'})
    info = info.find_all('p')
    main_info_cass = info[1].string.split('主演：')
    director = main_info_cass[0].split('：')[1]
    actor = main_info_cass[1]
    print(director, actor)
    main_info_area = info[2].string.split()
    area = main_info_area[0]
    time = int(main_info_area[2][0:-2])
    available_time = main_info_area[3].split('上映')[0]
    print(area, time, available_time)
    main_info_data = soup.find('ul', attrs={'class': 'data-list clearfix'})
    if main_info_data == None:
        continue
    else:
        main_info_data1 = main_info_data.find_all('p', attrs={'class': 'num'})[2].contents[0]
        main_info_data2 = main_info_data.find_all('p', attrs={'class': 'num'})[2].find('span').string
        main_info_data = main_info_data1 + main_info_data2
        print(main_info_data)
        list = [title, director, actor, time, area]
        c.execute('''
        INSERT INTO MOVIEINFO (ID,DIRECTOR,ACTOR,AREA,TIME)
        VALUES(?,?,?,?,?);
        ''', (id, list[1], list[2], list[4], list[3]))
        conn.commit()

conn.close()
