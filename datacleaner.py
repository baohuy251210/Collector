"""[datacleaner.py]
9/3/20'
Clean and process the init raw panel (aka uofucovidinit_timeline.csv)
"""

import csv
import pandas as pd
from datetime import datetime


def cases_process():

    def dateparse(x): return datetime.strptime(x, '%Y-%m-%d %H:%M')
    rawdf = pd.read_csv("./data/uofucovidinit_timeline.csv",
                        date_parser=dateparse, parse_dates=['time'])
    rawdf['time'] = rawdf['time'].dt.date
    # print(rawdf['time'])
    # rawpd['time'] = object, keep date only
    print('----data preprocessing (cumulative counts)-----')
    csv_name = './data/uofucovidinit_timeline.csv'
    # for row in rawdf['retrieved'][3:]:
    # print(int(row.split('|')[5]))
    new_cases = int(rawdf.iloc[-1]['retrieved'].split('|')[5])
    new_date = str(rawdf.iloc[-1]['time'])
    # compare with last row
    with open('./data/cases_timeline.csv', 'r') as csv_readfile:
        reader = csv.DictReader(csv_readfile)
        lastrow = list(reader)[-1]
        old_cases = int(lastrow['cases'])
        old_date = (lastrow['date'])

    # print(new_date, " ", old_date)
    # print(type(new_date), " ", type(old_date))

    if (old_cases != new_cases or old_date != new_date):
        with open('./data/cases_timeline.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([new_date, new_cases])
            print('(cleaner) New cases processed:')
            print(new_date, " | ", new_cases)
    else:
        print('(cleaner)No new cases detected')


"""processed data table:
date, cases(cumulative)  
"""


# -------MAIN----------
def main():
    pd.set_option('display.max_colwidth', None)
    cases_process()


if __name__ == "__main__":
    main()
