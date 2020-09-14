from scrape_match import scrape_match
import json

with open("links20000pages.json") as f_in:
    links=json.load(f_in)

with open('result_test.json', 'w') as f:   
    for d, L in links.items():
        for i in L:
            print(i)
            try:
                temp=scrape_match(i)
                temp['date']=d
                json.dump(temp, f)
            except Exception as e:
                print(f'Error {str(e)} with link {i}')
                continue
    