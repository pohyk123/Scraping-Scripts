from lxml import etree
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests
import time
import urllib

URL = 'https://api.telegram.org/bot{}/'.format('534846607:AAFbhdquVEshTeVsCqYS2RNtc8HiPea8lgc')

def get_url(url,payload=None):
    response = requests.get(url, params=payload)
    content = response.content.decode('utf8')
    return content

def sendMessage(text,chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
    get_url(url)

state=['28/28','28/28','28/28']
previousState=['28/28','28/28','28/28']
crawl_count = 0
iter_count = 0

while True:
    iter_count += 1

    try:
        if (iter_count%1000==0):
            raise Exception('[DEBUG - BADMINTON SLOTS TRACKING SCRIPT]')

        response=requests.get('https://www.union.ic.ac.uk/acc/badminton/sessions/index.php')
        content = response.content.decode('utf8')
        tableString=Selector(response=response).xpath('//div[@class="table-wrapper"]').extract()[1]

        message=''
        schedule=[]
        thuSesh=[]
        headers=['Date','Time','Location','Managers','Places','Additional Info','Operations']

        table = etree.HTML(tableString).find('body/div/table')
        element = table.find('thead')
        table.remove(element)
        element = table.find('tfoot')
        table.remove(element)
        rows = iter(table)
        for row in rows:
            daySchedule=[]
            for i in range(len(row)):
                    daySchedule.append(row[i].text)
            schedule.append(dict(zip(headers, daySchedule)))

        for i in range(len(schedule)):
            if('Thu' in schedule[i]['Date']):
                thuSesh.append(schedule[i])

        for i in range(len(thuSesh)):
            state[i]=thuSesh[i]['Places']
            if(state[i]!=previousState[i]):
                message+=thuSesh[i]['Date']
                message+=': '
                message+=previousState[i]+' -> '+state[i]
                message+='\n'
            if(previousState[i]=='0/28' and state[i]!='0/28'):
                message+=('Free open slots!!\n')
                message+=(thuSesh[i]['Date']+' - '+thuSesh[i]['Places'])
            previousState[i] = state[i]

        print(previousState)
        if(message!=''):
            sendMessage(message,153204542)
            sendMessage(message,119321447)

        crawl_count+=1

    except Exception as e:
        try:
            sendMessage(('/'.join(e.args))+'\n'+'Crawl Count: '+ str(crawl_count) + '\nTotal Iteration Count: ' + str(iter_count) + ' (x0.999=' + str(int(iter_count*0.999)) + ')',153204542)
        except:{}

    time.sleep(5)


# for i in len(schedule):
#     if schedule[i]
