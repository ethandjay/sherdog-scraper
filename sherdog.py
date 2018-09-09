#!/usr/bin/env python3
import requests
import random
import re
import pprint
import multiprocessing
import csv
import os
from joblib import Parallel, delayed
from bs4 import BeautifulSoup
from csv import DictWriter


__author__ = "Ethan Jaynes"
__version__ = "0.1.0"


def strip_method(full_method):

    match = re.search(r'\s*(.*)\s\((.*)\)', full_method)
    if match:
        method = match.group(1)
        method_by = match.group(2)
    else:
        method = full_method
        method_by = "N/A"


    return (method, method_by)

def request_event(url):

    base_url = "http://www.sherdog.com"

    r = requests.get(base_url + url)
    
    event_soup = BeautifulSoup(r.text, "lxml")

    """ 
    Match Return Schema:

    {
        winner:
        loser:
        method:
        method_by:
        referee:
        round_num:
        time:
        event:
        date:
        location:
    }
    """
    match_return = []

    # Get event info
    event = event_soup.find_all('meta', {"property" : "og:title"})[0]['content']
    print(f'Processing {event}...')
    date = event_soup.select('.authors_info')[0].select('.date')[0].contents[-1]
    location = event_soup.find_all('span', {"itemprop" : "location"})[0].string

    if "CANCELED" in location.upper():
        return None

    # Get and parse main fight
    winner = event_soup.select('.fight')[0].select('.left_side')[0].h3.span.string
    loser = event_soup.select('.fight')[0].select('.right_side')[0].h3.span.string

    details = event_soup.select('.resume')[0].find('tr').find_all('td')
    full_method = details[1].contents[-1]

    method, method_by = strip_method(full_method)

    referee = details[2].contents[-1].lstrip()
    round_num = details[3].contents[-1].lstrip()
    time = details[4].contents[-1].lstrip()

    match_return.append({
        'winner': winner,
        'loser': loser,
        'method': method,
        'method_by': method_by,
        'referee': referee,
        'round_num': round_num,
        'time': time,
        'event': event,
        'date': date,
        'location': location
    })

    match_list = event_soup.select('.event_match')[0].div.table.tbody.find_all('tr')

    # Pop header tr
    match_list.pop(0)

    for match in match_list:
        contents = match.contents
        fighters = (contents[3], contents[7])

        winner = fighters[0].div.a.span.string
        loser = fighters[1].div.a.span.string

        details = contents[9].contents
        full_method = details[0]

        method, method_by = strip_method(full_method)

        referee = details[-1].string
        round_num = contents[11].string
        time = contents[13].string

        match_return.append({
            'winner': winner,
            'loser': loser,
            'method': method,
            'method_by': method_by,
            'referee': referee,
            'round_num': round_num,
            'time': time,
            'event': event,
            'date': date,
            'location': location
        })

    print(f'Done processing {event}')
    print()

    return match_return
    



def main():

    
    
    event_links = []
    k = 1
    print('Gathering event listings...')
    while True:

        ufc_page = requests.get(f"http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2/recent-events/{k}")

        ufc_page_soup = BeautifulSoup(ufc_page.text, "lxml")

        recent_list = ufc_page_soup.select('div#recent_tab')[0].table

        recent_list = recent_list.find_all('tr')

        # If only header, no content
        if len(recent_list) == 1:
            break;

        # Remove header tr
        recent_list.pop(0)

        # String event links from onlick attr
        event_links.extend([row.get('onclick')[19:][:-2] for row in recent_list])

        k = k + 1;

    print('Event listings successfuly gathered')

    num_cores = multiprocessing.cpu_count()
    event_list = Parallel(n_jobs=num_cores, backend='threading')(delayed(request_event)(link) for link in event_links[:200])
    event_list = filter(None, event_list)

    print('Creating spreadsheet...')

    this_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(this_dir, 'matches.csv')
    with open(file_path, 'w', newline='') as f:
        fnames = ['winner','loser','method','method_by','referee','round_num','time','event','date','location']
        writer = csv.DictWriter(f, fieldnames=fnames)    


        writer.writeheader()
        for event in event_list:
            for match in event:
                writer.writerow(match)

    print('Complete')
    exit()

if __name__ == "__main__":
    main()