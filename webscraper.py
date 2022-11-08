
import urllib.request,sys,time
import requests
import pandas as pd
import random 
from collections import OrderedDict
from bs4 import BeautifulSoup
from itertools import product
from pprint import pprint

# might have to randomize header to avoid google block
# List of header that contain User-Agent
def list_dict():
    # Get headers list
    headers_list = [
        # Firefox 24 Linux
        {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
        # Firefox Mac
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    ]
    # Create ordered dict from Headers above
    ordered_headers_list = []
    for headers in headers_list:
        h = OrderedDict()
        for header,value in headers.items():
            h[header]=value
        ordered_headers_list.append(h)
    return ordered_headers_list

def random_header():
    headers_list = list_dict()
    headers = random.choice(headers_list)
    return headers

def scrape():
    # Modify with appropriate searches
    animals = ['Elephant', 'Tiger', 'calf']
    action = ['kill', 'kills' , 'killed', 'dead', 'death', 'dies', 'tusker', 'poacher', 'shot', 'electrocuted', 'found dead', 'tusks', 'injured', 'electrocution', 'poisoned', 'ivory']
    countries = ['Indonesia', 'Sri-lanka', 'Sri lanka', 'India', 'Malaysia', 'Thailand']
    
    df = pd.DataFrame()
    date_published = []
    title = []
    source = []
    article = []
    urls = []

    search_list = [' '.join(p) for p in product(animals, action, countries)]
    #pprint(search_list)

    search = search_list[1]
    search = "+".join(search.split(" "))
    r = requests.Session()
    # set query for google
    headers = random_header()
    r.headers = headers
    url = f"https://www.google.com/search?q={search}&tbm=nws&sxsrf=ALiCzsa4bRMelGaUbU51s8NChWBoZW4-5Q:1666938075523&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwiTqOqepIL7AhUlIX0KHcQFDagQpwV6BAgBEBY&biw=1689&bih=1284&dpr=1"
    res = r.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select(".dbsr a")
    print()

    """ for search in search_list:
        r = requests.Session()
        # set query for google
        headers = random_header()
        r.headers = headers
        url = f"https://www.google.com/search?q={search}&tbm=nws&sxsrf=ALiCzsa4bRMelGaUbU51s8NChWBoZW4-5Q:1666938075523&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwiTqOqepIL7AhUlIX0KHcQFDagQpwV6BAgBEBY&biw=1689&bih=1284&dpr=1"
        res = r.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select(".dbsr a")
        pprint(links) """

if __name__ == "__main__":
    print("Working\n")
    scrape()