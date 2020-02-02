#encoding=utf-8
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

#INPUT
with open("./data/compnames","r+",encoding='utf-8') as f:
    Corplist=f.read()
lines=Corplist.split()

res=[]
num=0
rules1=["银行","集团","控股","金融","证券","财务","投资","协会","公司","组织"]
for line in lines:
    scan=-1
    for rule in rules1:
        scan=line.find(rule)
        if scan!=-1:
            break
    if scan!=-1:
        newline=line[:scan+2]
    else:
        newline=line
    if newline not in lines:
        lines.append(newline)
for line in lines:
    print(line) 
    #sleep(2)
    #continue
#Sina
    q={}
    q['query']='site:sina.com.cn '+line
    url='https://news.sogou.com/news'
    requests.DEFAULT_RETRIES=5
    requests.session().keep_alive = False
    sleep(2)
    html=requests.get(url,params=q)
    sleep(2)
    html.encoding='gb18030'
    bs=BeautifulSoup(html.text,'lxml')
    print('Get Sogou!')
    for page in range(5):
        i=0
        print('Sina')
        while i<len(bs.select(".vrTitle a")):
            nurl=bs.select(".vrTitle a")[i]["href"]
            #print(nurl)
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            try:
                sleep(2)
                nhtml=requests.get(nurl)
                #nhtml=requests.get(nurl,timeout=(120,360))
                sleep(2)
                
            except:
                i+=1
                print('Get News Failure!')
                continue
            #print(3333333)
            nhtml.encoding='utf-8'
            nbs=BeautifulSoup(nhtml.text,'lxml')             
            try:
                #print(4444444)
                temp=[]
                title="".join(nbs.select(".main-title")[0].get_text().split())
                #print(title)
                date="".join(nbs.select(".date")[0].get_text().split())
                #print(date)
                src="".join(nbs.select(".source")[0].get_text().split())
                #print(123456)
                text="，".join(nbs.select(".article")[0].get_text().split(','))
                text="".join(text.split())
                text='\"'+text+'\"'
                findpx=text.rfind("px;}")
                findj=text.find("(jQuery);")
                findv=text.find("vote(默认)}")
                find2=text.find(";}")
                if findj!=-1:
                    text=text[findj+9:]
                elif findpx!=-1:
                    text=text[findpx+4:]
                elif findv!=-1:
                    text=text[findv+9:]
                #print(654312)
                href=nurl
                website='Sina'
                temp.append(str(num+1))
                temp.append(title)
                temp.append(date)
                temp.append(src)
                temp.append(text)
                temp.append(href)
                temp.append("Sina")
                temp.append(line)
                res.append(temp)
                num+=1
                i+=1
                #print(8989)
                with open("./dataset/SogouA.csv","a",encoding="gbk",errors="ignore") as tf:
                    tf.write('\"'+str(num)+'\",\"'+title+'\",\"'+date+'\",\"'+src+'\",\"'+text+'\",\"'+href+'\",\"'+website+'\",\"'+line+"\"\n") 
                print('Find!')       
            except:
                print('Find Failure!')                  
                i+=1
        try:
            next='https://news.sogou.com/news'+bs.select('#sogou_next')[0]["href"]
            #print(next)
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            sleep(2)
            #html=requests.get(next,timeout=(120,360))
            html=requests.get(next)
            print('Get Next!')
            sleep(2)
            html.encoding='gb18030'
            bs=BeautifulSoup(html.text,'lxml')
        except:
            print('Next Failure!')
            break
    sleep(1)
#Sohu
    q={}
    q['query']='site:sohu.com '+line
    url='https://news.sogou.com/news'
    requests.DEFAULT_RETRIES=5
    requests.session().keep_alive = False
    sleep(2)
    html=requests.get(url,params=q)
    sleep(2)
    html.encoding='gb18030'
    bs=BeautifulSoup(html.text,'lxml')
    for page in range(5):
        i=0
        print('Sohu')
        while i<len(bs.select(".vrTitle a")):
            nurl=bs.select(".vrTitle a")[i]["href"]
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            try:
                sleep(2)
                #nhtml=requests.get(nurl,timeout=(120,360))
                nhtml=requests.get(nurl)
                sleep(2)
                
            except:
                i+=1
                continue
            nhtml.encoding='utf-8'
            nbs=BeautifulSoup(nhtml.text,'lxml')             
            try:
                temp=[]
                title="".join(nbs.select(".text-title h1")[0].get_text().split())
                date=" ".join(nbs.select(".time")[0].get_text().split())
                src="".join(nbs.select(".user-info h4")[0].get_text().split())
                text="".join(nbs.select(".article")[0].get_text().split())
                text="，".join(text.split(','))
                text='\"'+text+'\"'
                href=nurl
                website='Sohu'
                temp.append(str(num+1))
                temp.append(title)
                temp.append(date)
                temp.append(src)
                temp.append(text)
                temp.append(href)
                temp.append("Sohu")
                temp.append(line)
                res.append(temp)
                num+=1
                i+=1
                with open("./dataset/SogouA.csv","a",encoding="gbk",errors="ignore") as tf:
                    tf.write('\"'+str(num)+'\",\"'+title+'\",\"'+date+'\",\"'+src+'\",\"'+text+'\",\"'+href+'\",\"'+website+'\",\"'+line+"\"\n")
                print('Find!')
            except:
                pass                   
                i+=1
        try:
            next='https://news.sogou.com/news'+bs.select('#sogou_next')[0]["href"]
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            sleep(2)
            #html=requests.get(next,timeout=(120,360))
            html=requests.get(next)
            sleep(2)
            print('Get next')
            html.encoding='gb18030'
            bs=BeautifulSoup(html.text,'lxml')
        except:
            break
    sleep(1)
#Tencent
    q={}
    q['query']='site:qq.com '+line
    url='https://news.sogou.com/news'
    requests.DEFAULT_RETRIES=5
    requests.session().keep_alive = False
    sleep(2)
    html=requests.get(url,params=q)
    sleep(2)
    html.encoding='gb18030'
    bs=BeautifulSoup(html.text,'lxml')
    for page in range(5):
        i=0
        while i<len(bs.select(".vrTitle a")):
            nurl=bs.select(".vrTitle a")[i]["href"]
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            try:
                sleep(2)
                #nhtml=requests.get(nurl,timeout=(120,360))
                nhtml=requests.get(nurl)
                sleep(2)
            except:
                i+=1
                continue
            nhtml.encoding='gb18030'
            nbs=BeautifulSoup(nhtml.text,'lxml')             
            try:
                temp=[]
                title="".join(nbs.select(".LEFT h1")[0].get_text().split())
                date=" "
                src="腾讯网"
                text="".join(nbs.select(".content-article")[0].get_text().split())
                text="，".join(text.split(','))
                text='\"'+text+'\"'
                href=nurl
                website='Tencent'
                temp.append(str(num+1))
                temp.append(title)
                temp.append(date)
                temp.append(src)
                temp.append(text)
                temp.append(href)
                temp.append("Tencent")
                temp.append(line)
                res.append(temp)
                num+=1
                i+=1
                with open("./dataset/SogouA.csv","a",encoding="gbk",errors="ignore") as tf:
                    tf.write('\"'+str(num)+'\",\"'+title+'\",\"'+date+'\",\"'+src+'\",\"'+text+'\",\"'+href+'\",\"'+website+'\",\"'+line+"\"\n")
            except:
                pass                   
                i+=1
        try:
            next='https://news.sogou.com/news'+bs.select('#sogou_next')[0]["href"]
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            sleep(2)
            #html=requests.get(next,timeout=(120,360))
            html=requests.get(next)
            sleep(2)
            html.encoding='gb18030'
            bs=BeautifulSoup(html.text,'lxml')
        except:
            break
    sleep(1)
#ifeng
    q={}
    q['query']='site:ifeng.com '+line
    url='https://news.sogou.com/news'
    requests.DEFAULT_RETRIES=5
    requests.session().keep_alive = False
    sleep(2)
    html=requests.get(url,params=q)
    sleep(2)
    html.encoding='gb18030'
    bs=BeautifulSoup(html.text,'lxml')
    for page in range(5):
        i=0
        while i<len(bs.select(".vrTitle a")):
            nurl=bs.select(".vrTitle a")[i]["href"]
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            try:
                sleep(2)
                #nhtml=requests.get(nurl,timeout=(120,360))
                nhtml=requests.get(nurl)
                sleep(2)
            except:
                i+=1
                continue
            nhtml.encoding='utf-8'
            nbs=BeautifulSoup(nhtml.text,'lxml')             
            try:
                temp=[]
                title="".join(nbs.select("#artical_topic")[0].get_text().split())
                date="".join(nbs.select(".ss01")[0].get_text().split())
                src="".join(nbs.select(".ss03")[0].get_text().split())
                text="".join(nbs.select('#main_content')[0].get_text().split())
                text="，".join(text.split(','))
                findpx=text.rfind("px;}")
                findj=text.rfind(");")
                findv=text.find("vote(默认)}")
                find2=text.rfind(";}")
                if findj!=-1:
                    text=text[findj+2:]
                elif findpx!=-1:
                    text=text[findpx+4:]
                elif find2!=-1:
                    text=text[findv+2:]
                findjt=text.rfind("<!--varcode_list")
                if findjt!=-1:
                    text=text[:findjt]
                text='\"'+text+'\"'
                href=nurl
                website='ifeng'
                temp.append(str(num+1))
                temp.append(title)
                temp.append(date)
                temp.append(src)
                temp.append(text)
                temp.append(href)
                temp.append("ifeng")
                temp.append(line)
                res.append(temp)
                num+=1
                i+=1
                with open("./dataset/SogouA.csv","a",encoding="gbk",errors="ignore") as tf:
                    tf.write('\"'+str(num)+'\",\"'+title+'\",\"'+date+'\",\"'+src+'\",\"'+text+'\",\"'+href+'\",\"'+website+'\",\"'+line+"\"\n")
            except:
                pass                   
                i+=1
        try:
            next='https://news.sogou.com/news'+bs.select('#sogou_next')[0]["href"]
            requests.DEFAULT_RETRIES=5
            sleep(2)
            requests.session().keep_alive = False
            sleep(2)
            #html=requests.get(next,timeout=(120,360))
            html=requests.get(next)
            sleep(2)
            html.encoding='gb18030'
            bs=BeautifulSoup(html.text,'lxml')
        except:
            break
    sleep(1)
#163
    q={}
    q['query']='site:163.com '+line
    url='https://news.sogou.com/news'
    requests.DEFAULT_RETRIES=5
    requests.session().keep_alive = False
    sleep(2)
    html=requests.get(url,params=q)
    sleep(2)
    html.encoding='gb18030'
    bs=BeautifulSoup(html.text,'lxml')
    for page in range(5):
        i=0
        while i<len(bs.select(".vrTitle a")):
            nurl=bs.select(".vrTitle a")[i]["href"]
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            try:
                sleep(2)
                #nhtml=requests.get(nurl,timeout=(120,360))
                nhtml=requests.get(nurl)
                sleep(2)
            except:
                print('Get Failed!')
                i+=1
                continue
            nhtml.encoding='gbk'
            nbs=BeautifulSoup(nhtml.text,'lxml')             
            try:
                #print(23333)
                temp=[]
                #print(12)
                title="".join(nbs.select(".post_content_main h1")[0].get_text().split())
                #print(title)
                posttimesource=nbs.select(".post_time_source")[0].get_text().split()
                #print(34)
                date=posttimesource[0]+' '+posttimesource[1]
                #print(45)
                src=posttimesource[3]
                text="".join(nbs.select(".post_text")[0].get_text().split())
                text="，".join(text.split(','))
                findf=text.rfind('(function')
                findh=text.rfind('.houseJrtt')
                findc=text.rfind('查看投顾')
                if findf!=-1:
                    text=text[:findf]
                elif findh!=-1:
                    text=text[:findh]
                elif findc!=-1:
                    text=text[:findc]
                text='\"'+text+'\"'
                href=nurl
                website='163'
                temp.append(str(num+1))
                temp.append(title)
                temp.append(date)
                temp.append(src)
                temp.append(text)
                temp.append(href)
                temp.append("163")
                temp.append(line)
                res.append(temp)
                num+=1
                i+=1
                #print(6666666)
                with open("./dataset/SogouA.csv","a",encoding="gbk",errors="ignore") as tf:
                    tf.write('\"'+str(num)+'\",\"'+title+'\",\"'+date+'\",\"'+src+'\",\"'+text+'\",\"'+href+'\",\"'+website+'\",\"'+line+"\"\n")
                #print(7777777)
            except:
                pass                   
                i+=1
                #print('Next Failed!')
        try:
            next='https://news.sogou.com/news'+bs.select('#sogou_next')[0]["href"]
            requests.DEFAULT_RETRIES=5
            requests.session().keep_alive = False
            sleep(2)
            #html=requests.get(next,timeout=(120,360))
            html=requests.get(next)
            sleep(2)
            html.encoding='gb18030'
            bs=BeautifulSoup(html.text,'lxml')
        except:
            break
    sleep(2)
    if num%2==0:
        sleep(2)
    if num%3==0:
        sleep(5)
    if num%5==0:
        sleep(10)
    if num%10==0:
        sleep(20)
    if num%20==0:
        sleep(40)
    if num%50==0:
        sleep(60)
"""
with open("sg.txt","w",encoding='utf-8') as f:
    f.write(str(bs.get_text()))
"""

with open("./dataset/SogouNew.csv","w",encoding="gbk",errors="ignore") as f:
    csvf=csv.writer(f)
    csvf.writerow(["number","title","date","source","text","href","website","corpname"])
    for row in res:
        csvf.writerow(row)
