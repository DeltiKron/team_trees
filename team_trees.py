#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import dirname, join

import requests
import datetime
import re
from bs4 import BeautifulSoup

def get_count():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    res = requests.get("http://teamtrees.org",headers=headers)
    doc = res.content.decode()
    soup = BeautifulSoup(doc, 'html.parser')
    total_tag = soup.find_all('div', attrs={'id': 'totalTrees'})
    total = total_tag[0]['data-count']
    return int(total)
    
if __name__ == "__main__":
    count =  get_count()
    date = datetime.datetime.now()
    print(date,count)
    directory = dirname(__file__)
    with open(join(directory, "team_trees_count.csv"),"a+") as outfile:
        outfile.write(f"{date},{count}\n")
