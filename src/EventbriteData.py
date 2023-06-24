import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# url = "https://www.eventbrite.com/d/germany--berlin--12435/all-events/"
url = "https://www.eventbrite.com/d/germany--berlin/all-events/"


page = 100
while page <= 135 :
    # Create a DataFrame to store all the events data in Berlin
    events_berlin = pd.DataFrame()

    print('Page {}...'.format(page))
    soup = BeautifulSoup(requests.get(url, params={'page': page}).content, 'html.parser')
    # print("This is soup: ",soup)
    # b = soup.find("script", {"type":"application/ld+json"}).contents
    # b = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
    b = [json.loads(x.string) for x in soup.find_all("script", type="application/ld+json")]

    # Create a dic to store info of every single event
    event = {}
    event['page'] = page
    if not b:
        print(f'This is a break for Page {page}!')
        break

    for item in b:
        if item == {}:
            pass
        else:
            event['startDate'] = item['startDate']
            event['endDate'] = item['endDate']
            event['name'] = item['name']
            event['url'] = item['url']
            event['addressCountry'] = item['location']['address']['addressCountry']
            event['addressLocality'] = item['location']['address']['addressLocality']
            event['addressRegion'] = item['location']['address']['addressRegion']
            event['streetAddress'] = item['location']['address']['streetAddress']
            event['postalCode'] = item['location']['address']['postalCode']
            event['latitude'] = item['location']['geo']['latitude']
            event['longitude'] = item['location']['geo']['longitude']
            event['locationName'] = item['location']['name']
            # event['description'] = item['description']

            event_df = pd.DataFrame([event])
            events_berlin = pd.concat([events_berlin, event_df], ignore_index=True)
    events_berlin.to_csv(f'./data/events_berlin/page{page}.csv')
    page += 1
    time.sleep(10)

# events_berlin.to_csv('./data/events_berlin.csv')
# print(events_berlin)