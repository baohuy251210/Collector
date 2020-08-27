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
import time


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
        field_names = ['time-MDT', 'retrieved']
        writer = csv.writer(csv_file)
        writer.writerow(field_names)
        writer.writerow([str(time), init])
    print('NEW INIT Created, this will recreate csv files')


def create_datacsv():
    """
    since retriever function return a list
    We'll derive only the number of self-reported case.
    """
    '''
    We only have data about self-reported case for now:
    see uofucovidinit_timeline.csv for full details on scraping
    '''

    csv_name = './data/uofucovid_timeline.csv'
    selfreport_cases = int(retrieve_covidpanel()[3].split()[0])
    time = datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M')

    with open(csv_name, 'w', encoding='utf-8') as csv_file:
        field_names = ['time-MDT', 'self-reported cases']
        writer = csv.writer(csv_file)
        writer.writerow(field_names)
        writer.writerow([str(time), selfreport_cases])

    print('uofucovid_timeline.csv created')


# create_datacsv()
# print(datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M'))
# create_initcsv()
# print(retrieve_covidpanel())


def updater_initcsv():
    """
    This updates the csv if the covid panel is different.
    Could be useful if the html changes the order. (to redo the retriever)
    """
    print('\n---covid panel scrape---')
    init_new = '|'.join(retrieve_covidpanel())
    time = datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M')
    init_old = ''
    # Read the current csv
    with open('./data/uofucovidinit_timeline.csv', 'r') as csv_readfile:
        reader = csv.DictReader(csv_readfile)
        lastrow = list(reader)[-1]
        init_old = lastrow['retrieved']

    if (init_old != init_new):
        print('(full)Detected new data')
        with open('./data/uofucovidinit_timeline.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([time, init_new])
            print('(full)New data updated')
    else:
        print('(full)No new update detected')


# updater_initcsv()

def updater_datacsv():
    """
    This function updates the cases count csv file
    """
    print('\n\n---cases scrape---')
    csv_name = './data/uofucovid_timeline.csv'
    selfreport_cases_new = int(retrieve_covidpanel()[3].split()[0])
    time = datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M')

    # compare with last row
    with open('./data/uofucovid_timeline.csv', 'r') as csv_readfile:
        reader = csv.DictReader(csv_readfile)
        lastrow = list(reader)[-1]
        selfreport_cases_old = lastrow['self-reported cases']

    if (int(selfreport_cases_old) != int(selfreport_cases_new)):
        print('(cases)Detected new data')
        with open('./data/uofucovid_timeline.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([time, selfreport_cases_new])
            print('(cases)New data updated')
    else:
        print('(cases)No new update detected')


def main():
    # ---SETTINGS---
    pd.set_option('display.max_colwidth', None)
    # ----------
    print("-------Scraping COVID-19 Data from UOFU---------- ")
    print(datetime.now(timezone('America/Denver')).strftime('%Y-%m-%d %H:%M:%S'))
    updater_initcsv()
    print(pd.read_csv(
        './data/uofucovidinit_timeline.csv'))

    time.sleep(0.5)  # Scraping ethics :-)

    updater_datacsv()
    print(pd.read_csv('./data/uofucovid_timeline.csv'))


if __name__ == "__main__":
    main()
