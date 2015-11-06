# -*- coding: utf-8 -*-
"""
Created on Thu Nov 05 14:15:33 2015

@author: balachandrd
"""
#%%

# See all the "as ..." contructs? They're just aliasing the package names.
# That way we can call methods like plt.plot() instead of matplotlib.pyplot.plot().
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas as pd
import time
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.notebook_repr_html', True)
import seaborn as sns
sns.set_style("whitegrid")
sns.set_context("poster")
import json
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
# The "requests" library makes working with HTTP requests easier
# than the built-in urllib libraries.
import requests
import string
import re
import collections
#%%
# Craiglist  Base Url

base_url="http://www.craigslist.org/about/sites#US"
craigslist_base = requests.get(base_url).text

#%%
# States dictionary will contain the state name as the key, the value will be a dictionary of all 
# cities and their URLS

#Defining filter for countries of interest in craigslist page
countries_filter=['CA', 'US']
country_dict={}

soup_main = BeautifulSoup(craigslist_base,"html.parser")

#Find all countries
countries_found = soup_main.findAll('h1')

#Loop over each country
for each_country in countries_found:
    country_name = each_country.find('a').get('name')
    
    if (country_name in countries_filter):
        
        cities_dict={}
        states_dict={}

        #The main page is divided in to columns of states/provinces
        #Traverse each column to obtain list of states        
        page_columns = each_country.findNextSibling('div', {'class':'colmask'}).findAll('div')
        for each_box in page_columns:
            #Find all states in each column
            for each_state in each_box.findAll('h4') :    
                #Find all cities
                all_cities = each_state.findNextSibling('ul').findAll('li')
                #Get city name and craiglist URL
                for each_city in all_cities :
                    city_name = str(each_city.find('a').text).lower()
                    city_url = each_city.find('a').get('href')
                    city_url = str(city_url)+'/search/bia?'
                    cities_dict[city_name] = city_url
                                    
                #print states_list
                state_name = str(each_state.text).lower()
                states_dict[state_name] = cities_dict
        country_dict[country_name] = states_dict

with open('C:/Users/balachandrd/Documents/Personal/CS-109/Project/DATA/craigslist_url.json', 'w') as json_url_file_w :
    json.dump(country_dict, json_url_file_w) 
#%% 
# TEMP
# Get all listings under bicycle category for the city
# For each list, get the URL, scrape  for content
url_a = 'http://charlestonwv.craigslist.org/search/bia?query=cannondale'

search_result = requests.get(url_a)
#%%
soup_search = BeautifulSoup(search_result.content, "html.parser")
all_rows = soup_search.find('div',{'class':'content'}).findAll('p')
for each_row in all_rows:
    row_data=each_row.find('span',{'class':'txt'}).find('span',{'class':'pl'})
     
    time_a=row_data.find('time').get('datetime')
    
    
    

#%%

def search_listing(url_dict, country, state, city, search_text):
    if (country in url_dict.keys()) :
        temp_cntry = url_dict[country].values()
        if (state in temp_cntry.keys()) :
            temp_state  = temp_cntry[state]
            if (city in temp_state.keys()) :
                city_url = tempstate[city]
    

     url_to_search = str(city_url)+"?query="+str(search_text)
     search_result = requests.get(url_a)

