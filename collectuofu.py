'''
This file collect the coronavirus.utah.edu
cases on-campus
'''

import requests
import urllib.request
from datetime import datetime
import bs4
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv
from pytz import timezone


def mainpage_status():
    '''
    return the connection status from here to
    c.utah.edu mainpage
    '''
    url = 'https://coronavirus.utah.edu/'
    response = requests.get(url)
    print('Status check: '+response)


def retrieve_covidpanel():
    '''
    Return a list of strings from the anticipated covid-19 panel
    '''
    url = 'https://coronavirus.utah.edu/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # finderstring is finding an object that might indicate the covid-19 counts:
    finder = (soup.find(string=re.compile(
        'positive COVID-19 cases', re.IGNORECASE)).parent)
    covidpanel = finder.parent
    return [str(e).lower() for e in covidpanel.descendants if (e != '\n' and type(e) is bs4.element.NavigableString)]


# print(retrieve_covidpanel())
# print(type("sds"))
'''
------------To CSV and Data tables--------------
'''


def create_initcsv():
    """one time use: init a csv for data storing 
    data/uofucovidinit_timeline.csv
    data/uofucovid_timeline.csv
    """
    init = '\n'.join(retrieve_covidpanel())
    # print(init)
    time = datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M')
    csv_name = './data/uofucovidinit_timeline.csv'
    with open(csv_name, 'w', encoding='utf-8') as csv_file:
        field_names = ['time', 'retrieved']
        writer = csv.writer(csv_file)
        writer.writerow(field_names)
        writer.writerow([str(time), init])


# print(datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M'))
create_initcsv()
# print(retrieve_covidpanel())
