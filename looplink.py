from scrape_match import scrape_match
import json

with open("pages_links.json") as f_in:
    links=json.load(f_in)
    
# start=False
with open('new_data.json', 'a') as f:   
    for d, L in links.items():
        for i in L:
            # if i=="https://www.hltv.org/matches/2315120/lgd-vs-wg-extremesland-2017-china-regional-finals":
            #     start=True
            print(i)
            # if start:
            try:
                temp=scrape_match(i)
                temp['date']=d
                json.dump(temp, f)
            except Exception as e:
                print(f'Error {str(e)} with link {i}')
                continue
