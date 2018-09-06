#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup


__author__ = "Ethan Jaynes"
__version__ = "0.1.0"


def main():

    ufc_page = requests.get("http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2")
    ufc_page_soup = BeautifulSoup(ufc_page.text, "lxml")

    recent_list = ufc_page_soup.select("div#recent_tab")[0].table





    print(recent_list.find_all("tr"))
    


if __name__ == "__main__":
    main()