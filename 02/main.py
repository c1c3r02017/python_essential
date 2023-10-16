#!/usr/bin/python
# -- coding: utf-8 -

# Scrapping
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import os
import requests
import re
import time

def get_html(icao):
    try:
        html = requests.get("https://aisweb.decea.mil.br/?i=aerodromos&codigo="+icao).content
        return BeautifulSoup(html, 'html.parser')
    except HTTPError as hp:
        print(hp)

def regex(txt):
    x = re.findall("[0-9][A-Z]+", txt)
    if x:
        return True
    return False

def solution(soup):
    response = {
    'cards':[],
    'sunrise':'',
    'sunset':'',
    'taf':'',
    'metar':''
    }

    # Search
    response['cards'] = soup.find_all(attrs={'onclick':"javascript:pageTracker._trackPageview('/cartas/aerodromos');"})
    response['sunrise'] = soup.find("sunrise" )
    response['sunset']  = soup.find("sunset" )
    div  = soup.find_all("p")

    try:
        aux = []
        for element in div:
            if regex(element.get_text()):
                aux.append(element)
        response['metar'] = aux[0]
        response['taf'] = aux[1]
    except:
        print('METAR or TAF Not Found')

    # Show results
    try:
        for card in response['cards']:
            print('Card: ',card.get_text())
        print('SUNRISE: ',response['sunrise'].get_text())
        print('SUNSET: ',response['sunset'].get_text())
        print('METAR: ',response['metar'].get_text())
        print('TAF: ',response['taf'].get_text())
    except:
        print('Not Found')


### MAIN ###
# Input ICAO
icao = input("ICAO: ").upper() #Example: ICAO = SBJD

# Clear console
clear = lambda: os.system('cls')
while True:
    try:
        clear()
        solution(get_html(icao))
        time.sleep(5)
    except:
        break
