import re
import requests
from bs4 import BeautifulSoup
# import json
# import MySQLdb as mdb
import csv
import itertools
import time
import os
from os.path import expanduser
import sys
        
home = expanduser("~")
desktop = home+'/Desktop'
desktopCheck = os.path.isdir(home+"/Desktop")
directory = desktop if desktopCheck is True else home   

# db = mdb.connect('localhost','tim','Kissinger23','relodeIndeed')
# cursor = db.cursor()

print '\n\n\n\n\n'
what = raw_input('what: ')
print
where = raw_input('where: ')
print
keywords = raw_input('keywords: ')
print
title = raw_input('specific title: ')
print
specificFirm = raw_input('specific company: ')
print
jobType = raw_input('''job type: \n 
all job types\nfull-time\npart-time\ncontract\ninternship\ntemporary\n''')

salary = raw_input('salary or salary range: \nfor example: \"$50,000\" or \"$40K-$90K\"\n')

fromage = raw_input('''jobs published how long ago: \n\"any\" for anytime,
\"15\" past 15 days, 
\"7\" for past 7 days, 
\"3\" for past 3 days
\"1\" results since yesterday \n''')

if re.search('all',jobType,flags=re.IGNORECASE):
    jobType = 'all'
elif re.search('full',jobType,flags=re.IGNORECASE):
    jobType = 'fulltime'
elif re.search('part',jobType,flags=re.IGNORECASE):
    jobType = 'parttime'
elif re.search('con',jobType,flags=re.IGNORECASE):
    jobType = 'contract'
elif re.search('intern',jobType,flags=re.IGNORECASE):
    jobType = 'internship'
elif re.search('temp',jobType,flags=re.IGNORECASE):
    jobType = 'temporary'
    
if re.search('any|all',fromage,flags=re.IGNORECASE):
    fromage = 'any'
elif re.search('15|fif',fromage,flags=re.IGNORECASE):
    fromage = '15'
elif re.search('7|sev',fromage,flags=re.IGNORECASE):
    fromage = '7'
elif re.search('3|thre',fromage,flags=re.IGNORECASE):
    fromage = '3'
elif re.search('1|one|yes',fromage,flags=re.IGNORECASE):
    fromage = '1'
elif re.search('last|sin',fromage,flags=re.IGNORECASE):
    fromage = 'last'
print '\n\n\n'

time.sleep(.5)
print 'your request is processing....'

def reformatNumber(xperiod,xdash,x800,xperiod1,number):
    number = number.encode('utf-8').strip()
    if re.search(x800,number):
        number = number[0]+' ('+number[2:5]+') '+number[6:]
        print number
    elif re.search(xdash,number):
        number = '('+number[0:3]+') '+number[4:]
        print number
    elif re.search(xperiod,number):
        number = '('+number[0:3]+') '+number[4:7]+'-'+number[8:]
        print number
    elif re.search(xperiod1,number):
        number = number[0]+' ('+number[2:5]+') '+number[6:9]+'-'+number[10:]
        print number
    else:
        pass
    
def writeCsv():
    if not number:
        pass
    else:
        csvList.append([firmName,jobTitle,jobCity,jobState,number,names,bingNameSearch]) 
        with open(directory+'/'+what.upper()+where+'.csv','w') as f:
            writer = csv.writer(f,delimiter=',',quoting=csv.QUOTE_ALL)
            writer.writerow(['FIRM NAME','JOB TITLE','JOB CITY','JOB STATE','NUMBER','NAMES FROM LINKEDIN','URL FOR LINKEDIN DATA'])
            [writer.writerow(row) for row in csvList]
        # cursor.execute('INSERT into relodeIndeed (firmname,jobtitle,jobcity,jobstate,phoneNumber) values (%s, %s, %s, %s,%s)',
        #                (firmName,jobTitle,jobCity,jobState,number))
        
getInfo = lambda x,y,z: item.find_all(x,{y:z})[0].text.encode('utf-8').strip()
intgr = lambda x: int(x) if x.isdigit() else x

regNum = re.compile(r'[0-9]{3}-[0-9]{4}')
altRegNum = re.compile(r'.[0-9]{3}. ?[0-9]{3}-[0-9]{4}|[0-9]{3}[-\.][0-9]{3}[-\.][0-9]{4}')

url = 'http://www.indeed.com/search?q='+what+'&l='+where+'&sr=directhire'+'&as_any='+keywords+'&ttl=&jt='+jobType+'&salary='+salary+'&fromage='+fromage
r = requests.get(url)
soup = BeautifulSoup(r.content)
try:
    limit = soup.find_all(id='searchCount')[0].text.encode('utf-8').split()
except:
    time.sleep(1)
    sys.exit("\n\nINDEED.COM RETURNED NO RESULTS!\n\nPlease try Again.\n\n")

limit = [re.sub(',','',str(x)) for x in limit]
limit = [intgr(x) for x in limit]
searchLimit = 1001 if limit[5] >= 1000 else limit[5]+10

i = 0
testList = []
csvList = []
while i<searchLimit:
    try:
        url = 'http://www.indeed.com/search?q='+what+'&l='+where+'&sr=directhire'+'&as_any='+keywords+'&ttl=&jt='+jobType+'&salary='+salary+'&fromage='+fromage+'&start='+str(i)
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        gData = soup.find_all('div',{'class':'row'})
        for item in gData:
            try:
                firmInfo = [getInfo('span','class','company'),
                            getInfo('a','target','_blank'),
                            getInfo('span','class','location').strip()]
                firmName,jobTitle,jobCityState = firmInfo
                if jobCityState != 'United States':
                    jobCityState = re.sub('[0-9]*','',jobCityState).strip()
                    jobCityState = re.sub('\(.*\)','',jobCityState).strip()
                    jobCity = jobCityState[0:-4].encode('utf-8')
                    jobState = jobCityState[-2:].encode('utf-8')
                    jobCityPlus = re.sub(', ','+',jobCity)
                else:
                    jobCity = 'United States'
                    jobState = ''
                firmNamePlus = re.sub("\'",'',firmName)
                firmNamePlus = re.sub('\W','+',firmName)+'+'
                bingSearch = 'http://www.bing.com/search?q='+firmNamePlus+jobCity+'+'+jobState # try just jobCityState and compare     
                info = requests.get(bingSearch)
                moreSoup = BeautifulSoup(info.content)
                contactData = moreSoup.find_all('div',{'class':"b_factrow"})
                altContactData = moreSoup.find_all('div',{'class':'b_imagePair tall_xb'})
                altaltContactData = moreSoup.find_all('ul',{'class':'b_vList'})
                testList.append([firmName,jobTitle,jobCity,jobState])
                # for link in item('a',href=re.compile('^/rc/clk\?jk=|^.*clk\?|^.*\?r=1')):
                #     source = 'http://www.indeed.com'+link.get('href')
                #     post_url = 'https://www.googleapis.com/urlshortener/v1/url'
                #     payload = {'longUrl': source}
                #     headers = {'content-type':'application/json'}
                #     r = requests.post(post_url, data=json.dumps(payload), headers=headers)
                #     text = r.content
                #     site = str(json.loads(text)['id'])
                bingNameSearch = 'https://www.bing.com/search?q='+firmNamePlus+jobCity+'+'+jobState+'%20name%20site%3Alinkedin.com'
                nameReq = requests.get(bingNameSearch)
                nameSoup = BeautifulSoup(nameReq.content)
                namesList = []
                for n in nameSoup.find_all('li',{'class':'b_algo'}):
                    if re.search('^.* \|.*LinkedIn',n.text):
                        name = re.findall('^(.*) \|',n.text)[-1].encode('utf-8').title()
                        namesList.append(name)
                        names = str(namesList)
                        names = re.sub('(\')',' ',str(names))
                        names = names.translate(None,'\[\]').strip()
                for this in contactData:
                    if re.search(regNum,this.text):
                        number = re.findall(altRegNum,this.text)[0].encode('utf-8')
                        writeCsv()
                for z in altContactData:
                    if not contactData:
                        if re.search(altRegNum,z.text):
                            number = re.findall(altRegNum,z.text)[0].encode('utf-8')
                            writeCsv()
                for q in altaltContactData:
                    if not contactData:
                        if not altContactData:
                            if re.search(regNum,q.text):
                                number = re.findall(altRegNum,q.text)[0].encode('utf-8')
                                writeCsv()
                for num in moreSoup:
                    if not contactData:
                        if not altContactData:
                            if not altaltContactData:
                                if re.search(altRegNum,moreSoup.text):
                                    number = re.findall(altRegNum,moreSoup.text)
                                    for p in number:
                                        number = p.encode('utf-8')
                                    writeCsv()
                                else:
                                    number = re.findall(altRegNum,str(num))
                                    for z in number:
                                        number = z.encode('utf-8')
                                    writeCsv()
            except:
                pass
    except Exception as e:
        print e
        pass

    # db.commit()

    i+=10

# db.close()

newList = [list(x[0:2]) for x in csvList]
noReps = [x for x,_ in itertools.groupby(newList)]

if limit[5]>=1000:
    scrapeRate = float(len(noReps))/len(testList)*100

else:
    scrapeRate = float(len(noReps))/len(testList)*100
    
scrapeRateStat = '%.3f'%round(scrapeRate,3)

print '\n\n'
print 'SCRAPE RATES:'
print
stats = str(scrapeRateStat)+'% scrape rate'
print stats,#'-- Actual'

testStats = '%.3f'%(float(len(noReps))/len(testList)*100)
# print str(testStats)+'% scrape rate -- Test'
print

nonScraped = []
newList = [i[0:2] for i in csvList]
# print 'NON-SCRAPED DATA:'
print

seeNonScrapedData = raw_input('Want to see non-scraped data? y/n: ')
time.sleep(.5)
if seeNonScrapedData == 'y':
    print
    for x in testList:
        if x[0:2] not in newList:
            nonScraped.append([x])
            with open(directory+'/NON-scraped'+what.upper()+where+'.csv','w') as f:
                writer = csv.writer(f,delimiter=',',quoting=csv.QUOTE_ALL)
                [writer.writerow(row) for row in nonScraped]
            print '\n'
        else:
            pass
    print 'NON-scraped'+what.upper()+where+'.csv is ready in ',directory+'\n'
    print what.upper()+where+'.csv','is ready in',directory+'\n'
    print len(nonScraped),'out of',len(testList), 'were NOT scraped\n\n'

else:
    for x in testList:
        if x[0:2] not in newList:
            nonScraped.append([x])
        else:
            pass
    print '\n'
    print len(nonScraped),'out of',len(testList), 'were NOT scraped\n'
    print what.upper()+where+'.csv','is ready in',directory
    print '\n'


