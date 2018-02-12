from lxml import etree
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests
import time
import urllib
from bs4 import BeautifulSoup as soup
import random

URL = 'https://api.telegram.org/bot{}/'.format('534846607:AAFbhdquVEshTeVsCqYS2RNtc8HiPea8lgc')

def get_url(url,payload=None):
    response = requests.get(url, params=payload)
    content = response.content.decode('utf8')
    return content

def sendMessage(text,chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
    get_url(url)

crawl_count = 0
iter_count = 0
SearchDate=['2/17/2018','2/24/2018','3/3/2018']
EnglishDate=['17_02_2018','24_02_2018','03_03_2018']

while True:
    iter_count += 1

    try:
        for i in range(len(SearchDate)):
            if (iter_count%1000==0):
                raise Exception('[DEBUG - ETHOS SLOTS TRACKING SCRIPT]')
            payload = {'searchType':0,'SearchType':0,'PersistSearchTimes':False,'SiteID':1,'Activity':'2012','SearchDate':SearchDate[i],'EnglishDate':EnglishDate[i],'English_TimeFrom':'07_00','English_TimeTo':'22_00','Duration':'60','submitButton':'Search'}
            response=requests.get('https://www.imperial.ac.uk/sports/bookings/Search/PerformSearch',params=payload)
            content = response.content.decode('utf8')
            print(content)
            if(Selector(response=response).xpath('//table[@class="ActivitySearchResults sortable"]')!=[]):
                tableString=Selector(response=response).xpath('//table[@class="ActivitySearchResults sortable"]').extract()[0]
                message=''
                schedule=[]
                thuSesh=[]
                headers=['Time','Location','Cost']

                page=soup(tableString,'lxml')
                soupPg=soup.prettify(page)
                table = etree.HTML(soupPg).find('body/table/tbody')

                rows = iter(table)
                for row in rows:
                    daySchedule=[]
                    for i in range(len(row)):
                            daySchedule.append(row[i].text.strip())
                    schedule.append(dict(zip(headers, daySchedule)))

                messageInfo=''
                for i in range(len(schedule)):
                    messageInfo='Date: '+SearchDate[i]+'\nTime: '+schedule[i]['Time']+'\n'
                sendMessage('Available Slots!!!\n'+messageInfo,153204542)
            else:
                print('no slots\r')

            crawl_count+=1
            time.sleep(random.random()*5)
    except Exception as e:
        try:
            sendMessage(('/'.join(e.args))+'\n'+'Crawl Count: '+ str(crawl_count) + '\nTotal Iteration Count: ' + str(iter_count) + ' (x0.999=' + str(int(iter_count*0.999)) + ')',153204542)
        except:{}
        print('/'.join(e.args))
    print('Crawl Count='+str(crawl_count))
    time.sleep(10)


# for i in len(schedule):
#     if schedule[i]
