import requests
from bs4 import BeautifulSoup
from pyecharts import  Bar

ALL_DATA=[]
def parse_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5795.400 QQBrowser/10.2.2101.400'
    }
    response = requests.get(url,headers)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text,'html5lib')
    divs = soup.find('div',class_='conMidtab')
    tables = divs.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index ==0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            min_temp = tds[-2]
            temp = list(min_temp.stripped_strings)[0]
            ALL_DATA.append({"city":city,"min_temp":int(temp)})
            # print({"city":city,"temperature":temp})


def main():
    # url = 'http://www.weather.com.cn/textFC/db.shtml'
    urls = [
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]
    for url in urls:
        parse_page(url)

#分析数据
#根据最低气温进行排序
    ALL_DATA.sort(key=lambda data:data['min_temp'])

    data = ALL_DATA[0:10]
    cities = list(map(lambda x:x['city'],data))
    temps  = list(map(lambda x:x['min_temp'],data))
    #pyechars
    chart = Bar("中国天气最低气温排行榜")
    chart.add('天气',cities,temps)
    chart.render('temprature.html')


if __name__ == '__main__':
    main()