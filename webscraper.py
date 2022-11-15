
import urllib.request,sys,time
import requests
import pandas as pd
import random 
from bs4 import BeautifulSoup as Soup
from itertools import product
from pprint import pprint
import re
from datetime import datetime, timedelta
import random

# Define the the phrases to be searched on google, the
def random_header():
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
        ]
    header = {
        'User-Agent': random.choice(user_agents),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'Origin': 'https://www.google.com',
        'Connection': 'keep-alive'
        }
    return header

#Modify with appropriate searches
def search_terms():
    animals = ['Elephant', 'Tiger', 'calf']
    action = ['kill', 'kills' , 'killed', 'dead', 'death', 'dies', 'tusker', 'poacher', 'shot', 'electrocuted', 'found dead', 'tusks', 'injured', 'electrocution', 'poisoned', 'ivory']
    countries = ['Indonesia', 'Sri-lanka', 'Sri lanka', 'India', 'Malaysia', 'Thailand']
    return [' '.join(p) for p in product(animals, action, countries)]

def google_scrape():
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
        # change url so that it only shows english language, currently some other languages appear
        url = f"https://www.google.com/search?q={query}&tbm=nws&sxsrf=ALiCzsa4bRMelGaUbU51s8NChWBoZW4-5Q:1666938075523&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwiTqOqepIL7AhUlIX0KHcQFDagQpwV6BAgBEBY&biw=1689&bih=1284&dpr=1"
        
        while(url):
            # Requesting page and result
            header = random_header()
            req = urllib.request.Request(url, headers=header)
            try:
                response = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                print("URL:"+url)
                print("Header:"+header)
                raise e
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
                response.close()
                break
            response.close()

    df = pd.DataFrame(data={'title':titles, 'date': dates, 'article':articles, 'source':sources, 'links':links, 'query':queries, 'google url':search_urls})
    df.to_excel("scraped.xlsx")
    print("Success")


""" Cases:
Popup
Paywall
Article is in seperate blocks

Issues:
Difference between ' and ’

Assumptions:
soup.title finds the first title element anywhere in the html document
title.string assumes it has only one child node, and that child node is a string
 """
def title_scraper():
    full_title = []
    full_article = []
    df = pd.read_excel("scraped.xlsx")
    for index, row in df.iterrows():
        title = row.title
        if title.split()[-1] == "...":
            title = ' '.join(title.split()[:-1])
        url = row.links
        page = requests.get(url)
        html = page.text
        soup = Soup(html, "html.parser")
        #print("-----------------")
        #print(title)
        try:
            title = soup.title.string.strip()
        except:
            title = soup.find(text=re.compile(title))
        full_title.append(title)
        page.close()

""" Cases:
Popup
Paywall
Article is in seperate blocks

Issues:
Difference between ' and ’
 """
def article_scraper():
    full_title = []
    full_article = []
    df = pd.read_excel("scraped.xlsx")
    #for index, row in df.iterrows():
    for i in  range(11):
        title = df.title.iloc[i]
        if title.split()[-1] == "...":
            title = ' '.join(title.split()[:-1])
        url = df.urls.iloc[i]
        page = requests.get(url)
        html = page.text
        soup = Soup(html, "html.parser")
        #print("-----------------")
        #print(title)
        article = soup.find(text=re.compile(title))
        full_article.append(title)
        page.close()




if __name__ == "__main__":
    print("Working\n")
    #google_scrape()
    #title_scraper()
    article_scraper