
import urllib.request,sys,time
import requests
import pandas as pd
import random 
from collections import OrderedDict
from bs4 import BeautifulSoup as Soup, ResultSet
from itertools import product
from pprint import pprint
import re
from datetime import datetime, timedelta

# Define the the phrases to be searched on google, the
def search_terms():
    #Modify with appropriate searches
    animals = ['Elephant', 'Tiger', 'calf']
    action = ['kill', 'kills' , 'killed', 'dead', 'death', 'dies', 'tusker', 'poacher', 'shot', 'electrocuted', 'found dead', 'tusks', 'injured', 'electrocution', 'poisoned', 'ivory']
    countries = ['Indonesia', 'Sri-lanka', 'Sri lanka', 'India', 'Malaysia', 'Thailand']
    return [' '.join(p) for p in product(animals, action, countries)]

def scrape():
    dates = []
    titles = []
    sources = []
    articles = []
    links = []
    queries = []
    search_urls = []

    for query in search_terms():
        query = "+".join(query.split(" "))

        # set query for google news tab first page
        url = f"https://www.google.com/search?q={query}&tbm=nws&sxsrf=ALiCzsa4bRMelGaUbU51s8NChWBoZW4-5Q:1666938075523&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwiTqOqepIL7AhUlIX0KHcQFDagQpwV6BAgBEBY&biw=1689&bih=1284&dpr=1"
        
        while(url):
            # Requesting page and result
            header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}
            req = urllib.request.Request(url, headers=header)
            response = urllib.request.urlopen(req)
            page = response.read()
            content = Soup(page, "html.parser")
            results = content.find_all("a",{"jsname" : re.compile(r".*")})[3:-1]

            for result in results:

                # Grab relevant information from the search results
                title = result.find("div", {"role" : "heading"}).text.replace("\n","")
                link = result.get("href")
                article = result.find("div", {"role" : "heading"}).next_sibling.text
                date = result.find("div", {"role" : "heading"}).next_sibling.findNext('div').text
                hours = re.search(r'^\d+', date).group()
                date = datetime.now() - timedelta(hours = int(hours))
                source = result.find("div", {"role" : "heading"}).previous_sibling.findNext('span').text

                # Avoid duplicate articles by same queries
                if link not in links: 
                    titles.append(title)
                    articles.append(article)
                    links.append(link)
                    dates.append(date)
                    sources.append(source)
                    queries.append(query)
                    search_urls.append(url)

            # Checks if there is a next page of results
            try:
                # Example case Tiger dead India of having 2 pages
                url = "https://www.google.com" + content.find("a", id="pnnext").get("href")
            except:
                break
            response.close()

    df = pd.DataFrame(data={'title':titles,'query':queries, 'google url':search_urls})
    print(df)
    print("Success")


if __name__ == "__main__":
    print("Working\n")
    scrape()