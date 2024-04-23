import ssl
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import re
import queue
from bs4 import BeautifulSoup
from pymongo import MongoClient


def crawlerThread(frontier) :
    visited = []
    count = 0

    firstlink = "https://www.cpp.edu"
    while frontier:

        url = frontier.pop(0)

        if url not in visited:
            visited.append(url)

        the_html = retrieveHTML(url)


        if the_html.find('h1', string="Permanent Faculty"):
            print("permanent page found")
            frontier.clear()
        else:
            parsed = the_html.find_all('a')
            for link in parsed:
                just_link = link.get('href')

                if '/sci/computer-science/' in just_link:

                    if just_link.startswith('/'):
                        just_link = firstlink + just_link

                    if just_link not in visited and just_link not in frontier:
                        frontier.append(just_link)




def retrieveHTML(url):
    context = ssl._create_unverified_context()

    html = urlopen(url, context=context).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


seed = "https://www.cpp.edu/sci/computer-science/"
frontier = [seed]

crawlerThread(frontier)
