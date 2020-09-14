from bs4 import BeautifulSoup
import urllib.request as urllib2

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

site="https://www.hltv.org/matches/2343627/complexity-vs-nip-esl-pro-league-season-12-europe"

def scrape_match(link):
    
    site=link
    info={}
    info['match_page_link']=link
    req = urllib2.Request(site, headers=hdr)
    page=urllib2.urlopen(req)
    soup=BeautifulSoup(page,parser="lxml",features="lxml")

    #extracting teams info (name/logos url/page url)
    t1=soup.select_one('div.team1-gradient a').contents
    t2=soup.select_one('div.team2-gradient a').contents

    #print(list(map(lambda x:x.contents[1] if len(x)==2 else x.contents[0].contents[0],soup.select('div.teamRanking > .a-reset '))))
    a,b=list(map(lambda x:x.contents[1] if len(x)==2 else x.contents[0].contents[0],soup.select('div.teamRanking > .a-reset ')))
    team1={'name':t1[0]['title'],'logoUrl':t1[0]['src'],'teamPageUrl':"https://www.hltv.org"+soup.select_one('div.team1-gradient a')['href'],'ranking':a}
    team2={'name':t2[0]['title'],'logoUrl':t2[0]['src'],'teamPageUrl':"https://www.hltv.org"+soup.select_one('div.team2-gradient a')['href'],'ranking':b}

    
    #past5matches
    first=True
    pastmatches=soup.select('div.past-matches table.table.matches')
    for (j,x) in enumerate(pastmatches):
        k=len(x.select("td.opponent a"))
        teamsH=[x.select("td.opponent a")[i].contents[0] for i in range(k)]
        resultH=[x.select("td.spoiler.result")[i].get('class')[-1] for i in range(k)]
        scoreH=[x.select("td.spoiler.result")[i].contents[0] for i in range(k)]
        if first:
            team1['history']=list(zip(teamsH,resultH,scoreH))
            first=False
        else:
            team2['history']=list(zip(teamsH,resultH,scoreH))
    info['teams']=(team1,team2)
    #score
    score=soup.select_one('div.team1-gradient > div').contents[0]+"-"+soup.select_one('div.team2-gradient > div').contents[0]
    info['score']=score
    #head
    head=[int(*x.contents) for x in soup.select('.flexbox-column.flexbox-center.grow .bold')]
    info['headtohead']=head

    #map scores dict()=(mapname,score,teams pick)
    if soup.select_one('div.padding.preformatted-text')!=None:
        matchformat=soup.select_one('div.padding.preformatted-text').contents[0]
        info['format-matchinfo']=matchformat
    else:
        info['format-matchinfo']="no info"
    maps=soup.select(".mapholder")
    dictMaps={}
    
    #if soup.select_one('div.padding.preformatted-text').contents[0]!='Best of 1':
    for i,x in enumerate(maps):
        if x.select_one('.played')!=None:
            mapName=x.select_one('.mapname')
            mapScore=x.select('.results-team-score')
            mapPick=x.select_one('.pick img')
            dictMaps["map"+str(i+1)]=(mapName.contents[0],"-".join([x.contents[0] for x in mapScore]),mapPick['title'] if mapPick!=None else 'decider')
    info["map_scores_picks"]=dictMaps
    #match start time with gmt+1 time
    info['time']=soup.select_one(".timeAndEvent .time").contents[0]
    #print((soup.select_one(".timeAndEvent .event a")['href'],soup.select_one(".timeAndEvent .time")['title']))
    info['event']=(soup.select_one(".timeAndEvent .event a")['title'],"https://www.hltv.org"+soup.select_one(".timeAndEvent .event a")['href'])
    return info

#print(scrape_match("https://www.hltv.org/matches/2343647/g2-vs-ence-esl-pro-league-season-12-europe"))