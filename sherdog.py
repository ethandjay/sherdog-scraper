#!/usr/bin/env python3
import requests
import random
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool


__author__ = "Ethan Jaynes"
__version__ = "0.1.0"


def strip_method(full_method):
	match = re.search(r'\s(.*)\s\((.*)\)', full_method)
	method = match.group(1)
	method_by = match.group(2)

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
	match_return = {}

	# Get and parse main fight
	winner = event_soup.select('.fight')[0].select('.left_side')[0].h3.span.string
	loser = event_soup.select('.fight')[0].select('.right_side')[0].h3.span.string

	details = event_soup.select('.resume')[0].find('tr').find_all('td')
	full_method = details[1].contents[-1]

	method, method_by = strip_method(full_method)

	referee = details[2].contents[-1].lstrip()
	round_num = details[3].contents[-1].lstrip()
	time = details[4].contents[-1].lstrip()

	match_list = event_soup.select('.event_match')[0].div.table

	# Pop header tr
	match_list.pop(0)

	for match in match_list:
		fighters = match.find_all('col_fc_upcoming')
		for fighter in fighters:
			name = fighter.select('.fighter_result_data')[0].a.span

	return "hello"



def main():

    ufc_page = requests.get("http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2")
    ufc_page_soup = BeautifulSoup(ufc_page.text, "lxml")

    recent_list = ufc_page_soup.select('div#recent_tab')[0].table

    recent_list = recent_list.find_all('tr')

    # Remove header tr
    recent_list.pop(0)

    # String event links from onlick attr
    event_links = [row.get('onclick')[19:][:-2] for row in recent_list]

    # pool = Pool(4)

    # match_list = pool.map(request_event, event_links)

    for link in event_links:
    	request_event(link)


if __name__ == "__main__":
    main()