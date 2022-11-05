
import urllib.request,sys,time
import requests
import pandas as pd
import random 
from collections import OrderedDict
from bs4 import BeautifulSoup

# might have to randomize header to avoid google block

def scrape():
    # Modify with appropriate searches
    search_list = ['Elephant kill', 'Tiger kill', 'Elephant death','Tiger death']
    countries = ['Indonesia', 'Sri-lanka', 'Sri lanka', 'India', 'Malaysia', 'Thailand']

    sep = '.'
    
    df = pd.DataFrame()
    date_published = []
    title = []
    source = []
    article = []
    urls = []

    # Google needs headers so that it knows it's not a fake request
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    for search in search_list:
        r = requests.Session()
        # set query for google
        query = search.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}&tbm=nws&sxsrf=ALiCzsa4bRMelGaUbU51s8NChWBoZW4-5Q:1666938075523&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwiTqOqepIL7AhUlIX0KHcQFDagQpwV6BAgBEBY&biw=1689&bih=1284&dpr=1"
        res = r.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select(".dbsr a")
        print(links)

if __name__ == "__main__":
    print("Working\n")
    scrape()