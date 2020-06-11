
import pandas as pd
import requests
from bs4 import BeautifulSoup
# headers storage
headers = {
    'Host': 'dianying.nuomi.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cookie': 'Hm_lvt_022c6fcfbc81400674cdf480300687b5=1587629570; Hm_lpvt_022c6fcfbc81400674cdf480300687b5=1587683476; BAIDUID=526D6E959C18E36E6E507F5009F748B6:FG=1'


}
finallist = []
#这个是所有电影的爬虫， 因为绝大部分电影id 在10000-96699之间 所以取得这个范围值
for i in range(10000,96699):
    #将id变成5位数字
    i = str(i).zfill(5)
    url = 'https://dianying.nuomi.com/movie/detail?movieId='+i
    print(url)
    #解析
    strhtml = requests.get(url,headers = headers)
    soup = BeautifulSoup(strhtml.text,'lxml')
    #找所有信息父系tag
    data = soup.find('div', attrs={'class':"info"})
    title = data.find('h4').string
    #过滤空ID
    if title == None:
        continue
    #分离数据
    info = data.find('div',attrs = {'class':'content'})
    info = info.find_all('p')
    main_info_cass = info[1].string.split('主演：' )
    director = main_info_cass[0].split('：')[1]
    actor = main_info_cass[1]
    print(director,actor)
    main_info_area = info[2].string.split( )
    area = main_info_area[0]
    time = main_info_area[2]
    available_time = main_info_area[3].split('上映')[0]
    print(area,time,available_time)
    main_info_data = soup.find('ul',attrs = {'class':'data-list clearfix'})
    if main_info_data == None:
        continue
    else:
        main_info_data1 = main_info_data.find_all('p',attrs = {'class':'num'})[2].contents[0]
        main_info_data2 = main_info_data.find_all('p',attrs = {'class':'num'})[2].find('span').string
        main_info_data = main_info_data1+main_info_data2
        print(main_info_data)
        list = [title,director,actor,time,area,available_time]
        #最后都储存到finallist
        finallist.append(list)
#最后pandas 输出csv
result = pd.DataFrame(finallist,columns = {'名称':'','导演':'','主演':'','时长':'','地区':'','上映时间':''})
result.to_csv('result1.csv')
