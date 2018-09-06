#!/usr/bin/env python3
import requests
import random
from bs4 import BeautifulSoup
from multiprocessing import Pool


__author__ = "Ethan Jaynes"
__version__ = "0.1.0"



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
		round:
		time:
		event:
		date:
		location:
	}
	"""
	match_return = {}

	# Get main fight
	fighter1 = event_soup.select('.fight')[0].select('.left_side')[0].h3.span.string
	fighter2 = event_soup.select('.fight')[0].select('.right_side')[0].h3.span.string

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