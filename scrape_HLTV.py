from bs4 import BeautifulSoup
import urllib.request as urllib2
from scrape_match import scrape_match
import json

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def scrape_links_bydate(n=5):
    #print(n)
    dates_links={}
    for i in range(min(n,554)):
        print(i)
        if i==0:
            site="https://www.hltv.org/results"
            req = urllib2.Request(site, headers=hdr)
            page=urllib2.urlopen(req)
            soup=BeautifulSoup(page,parser="lxml",features="lxml")
            #all_dates=[x.contents[0][12:] for x in  soup.select('.results-sublist span:first-of-type.standard-headline')] 
            # print(all_dates)

            for i in soup.select_one("[data-zonedgrouping-headline-format=\"'Results for' MMMM do y\"]").select('.results-sublist'):
                #L=["https://www.hltv.org"+x['href'] for x in i.select('.result-con a')]
                date=i.select_one('.standard-headline').contents[0][12:]
                links=["https://www.hltv.org"+x['href'] for x in i.select('.result-con a')]
                dates_links[date]=links
        else:
            site="https://www.hltv.org/"+"results?offset="+str(100*i)
            req = urllib2.Request(site, headers=hdr)
            page=urllib2.urlopen(req)
            soup=BeautifulSoup(page,parser="lxml",features="lxml")
            #all_dates=[x.contents[0][12:] for x in  soup.select('.results-sublist span:first-of-type.standard-headline')] 
            # print(all_dates)
            for i in soup.select_one("[data-zonedgrouping-headline-format=\"'Results for' MMMM do y\"]").select('.results-sublist'):
                #L=["https://www.hltv.org"+x['href'] for x in i.select('.result-con a')]
                date=i.select_one('.standard-headline').contents[0][12:]
                links=["https://www.hltv.org"+x['href'] for x in i.select('.result-con a')]
                dates_links[date]=links
    return dates_links

datelinks=scrape_links_bydate(20000)
final=[]
with open('pages_links.json', 'w') as f:
    json.dump(datelinks, f)

for d, L in datelinks.items():
    for i in L:
        try:
            temp=scrape_match(i)
            temp['date']=d
            final.append(temp)
        except Exception as e:
            print(f'Error {str(e)} with link {i}')
            continue
        
with open('result_test.json', 'w') as f:
    json.dump(final, f)