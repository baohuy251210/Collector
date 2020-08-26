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
    init = '|'.join(retrieve_covidpanel())
    # print(init)
    time = datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M')
    csv_name = './data/uofucovidinit_timeline.csv'
    with open(csv_name, 'w', encoding='utf-8') as csv_file:
        field_names = ['time', 'retrieved']
        writer = csv.writer(csv_file)
        writer.writerow(field_names)
        writer.writerow([str(time), init])
    print('NEW INIT Created, this will recreate csv files')


# print(datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M'))
# create_initcsv()
# print(retrieve_covidpanel())

def updater_initcsv():
    """
    This updates the csv if the covid panel is different.
    Could be useful if the html changes the order. (to redo the retriever)
    """
    init_new = '|'.join(retrieve_covidpanel())
    time = datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M')
    init_old = ''
    # Read the current csv
    with open('./data/uofucovidinit_timeline.csv', 'r') as csv_readfile:
        reader = csv.DictReader(csv_readfile)
        lastrow = list(reader)[-1]
        init_old = lastrow['retrieved']

    if (init_old != init_new):
        print('Detected new data')
        with open('./data/uofucovidinit_timeline.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([time, init_new])
            print('New data updated')
    else:
        print('No new update detected')


updater_initcsv()
