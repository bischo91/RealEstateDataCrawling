import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import pandas as pd
import regex as re
import random
import sqlite3
from datetime import date
import datetime


def url_opener(url):
    chromedriver = "~/Downloads/chromedriver" # path to the chromedriver executable
    chromedriver = os.path.expanduser(chromedriver)
    sys.path.append(chromedriver)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('window-size=1920x1080');
    # options.add_argument("--headless");
    # options.add_argument('disable-gpu')
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    time.sleep(random.random()*10 + 10**random.random())
    driver = webdriver.Chrome(chromedriver, options=options)
    # driver.minimize_window()
    driver.get(url)
    time.sleep(random.random()*10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if "Please verify you're a human" in soup.text:
        print("Error from Please verify you're a human")
        print(url)
        time.sleep(random.random()*600)
        return None
    else:
        time.sleep(random.random()*100*random.random()+random.random())
        # driver.quit()
        return soup

def list_page_urls(pages, url):
    page_list = []
    for page in pages:
        if str(page.text).isnumeric():
            page_list.append(int(page.text))
    pages = []
    page_urls = []
    for pg in list(range(1,max(page_list)+1)):
        pages.append(str(pg))
        page_urls.append(url + str(pg) + "_p")
    return page_urls

def detailstr2data(detail):
    detail = detail.replace(',','')
    detail = detail.lower().replace('Square Feet','sqft')
    detail = detail.replace('bds', 'bd')
    detail = detail.replace('--','0')
    sqft = 0
    acres = 0
    property =''
    if 'lot' in detail.lower():
        property = 'lot'
        if 'acres' in detail.lower():
            detail = detail.lower().split('acres')
            # Need to fix ACRES instead of SQFT
            bds = 0
            ba = 0
            acres = float(detail[0])
        elif 'sqft' in detail.lower():
            detail = detail.lower().split('sqft')
            bds = 0
            ba = 0
            sqft = float(detail[0])
    elif 'studio' in detail.lower():
        property = 'studio'
        detail = detail.lower().split('studio')
        bds = 0
        detail = detail[1].split('ba')
        ba = detail [0]
        sqft = float(detail[1].replace(',','').replace('sqft',''))
    elif 'bd' and 'ba' and 'sqft' in detail.lower():
        property = 'house/condo'
        detail = detail.split('bd')
        bds = float(detail[0])
        detail = detail[1].split('ba')
        ba = float(detail[0])
        sqft = float(detail[1].split('sqft')[0])
    return bds, ba, sqft, acres, property

def price2data(price):
    price = price.replace(',','')
    price = price.replace('$','')
    est = False
    if 'est' in price.lower():
        est = True
        price = price.lower().replace('est.','')
    price = price.replace('+','')
    if price.isnumeric():
        return int(price), est
    else:
        return 0, est

def extract_and_store_data():
    url ='https://www.zillow.com/homes/for_sale/gainesville-fl/'
    url = 'https://www.zillow.com/homedetails/1790-NW-34th-St-Gainesville-FL-32605/87624841_zpid/'
    soup = url_opener(url)
    house_details = soup.find("ul", class_='ds-home-fact-list')
    # house_details = house_details.find_all('li',{"class": "ds-home-fact-list"})
    house_details = house_details.find_all('li')
    
    type, year_built, heating, cooling, parking, hoa = '','','','','',''
    for i in house_details:
        element = i.text
        print(element)
        element_list = element.split(':')
        # element_list[0]
        if element_list[0].lower() == 'type':
            type = element_list[1]
        elif element_list[0].lower() == 'year built':
            year_built = int(element_list[1])
        elif element_list[0].lower() == 'heating':
            heating = element_list[1]
        elif element_list[0].lower() == 'cooling':
            cooling = element_list[1]
        elif element_list[0].lower() == 'parking':
            parking = element_list[1]
        elif element_list[0].lower() == 'hoa':
            hoa = element_list[1].replace('$','').replace(',','')  # WHAT ABOUT HOA MONTHLY YEARLY QUARTERLY ETC?
    print(type)
    print(year_built)
    print(heating)
    print(cooling)
    print(parking)
    print(hoa)
    
    # house_details = house_details.text
    # house_details = house_details.lower()
    # house_details = house_details.split(':')
    # house_details = house_details.split('year built')
    # house_details = house_details.split('heating')
    # house_details = house_details.split('heating')
    # house_details = house_details.split('cooling')
    # house_details = house_details.split('parking')
    
    
    # print(house_details)
    
    

    # if soup != None:
    #     pages = []
    #     current_pg = 'invalid'
    #     next_pg = ''
    #     while next_pg != current_pg:
    #         current_pg = next_pg
    #         if current_pg == '':
    #             print('Page 1')
    #         else:
    #             print('Page ' + str(''.join(filter(lambda i: i.isdigit(), current_pg))))
    #         url_pg = url + current_pg
    #         pages.append(url_pg)
    #         soup = url_opener(url_pg)
    #         for element in soup.find_all(class_='list-card'):
    #             print(element)
    #             house_url = element.find("a", class_='list-card-link')
    #             house_url = house_url['href']
    #             price = element.select_one('.list-card-price').text
    #             price, est = price2data(price)
    #             new_price = price
    #             details = element.select_one('.list-card-details').text
    #             if house_url in saved_link:
    #                 j = saved_link.index(house_url)
    #                 last_price_change = ''
    #                 if int(new_price) == int(saved_price[j]):
    #                     prev_price = rows[j][15]
    #                     last_price_change = rows[j][14]
    #                 else:
    #                     # j=j+1
    #                     print("price updated for row id " + str(j+1))
    #                     prev_price = saved_price[j]
    #                     last_price_change = today_date
    #                 bds = rows[j][1]
    #                 ba = rows[j][2]
    #                 sqft = rows[j][3]
    #                 acres = rows[j][4]
    #                 est = rows[j][5]
    #                 property = rows[j][6]
    #                 type = rows[j][7]
    #                 year = rows[j][8]
    #                 heating = rows[j][9]
    #                 cooling = rows[j][10]
    #                 parking = rows[j][11]
    #                 hoa = rows[j][12]
    #                 # cursor_new.execute(sql_new, (new_price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, house_url, date_today, ''))
    #             else:
    #                 bds, ba, sqft, acres, property = detailstr2data(details)
    #                 if est == True:
    #                     est = 'Estimate'
    #                 else:
    #                     est = ''
    #                 time.sleep(random.random()*10+random.random()*(random.random()*10))
    #                 soup_house = url_opener(house_url)
    #                 labellist =[]
    #                 valuelist =[]
    #                 # factlabel_span = soup_house.find_all("span", {"class":"ds-home-fact-label"})
    #                 # factvalue_span = soup_house.find_all("span", {"class":"ds-home-fact-value"})
    #                 house_details = soup_house.find("ul", class_='ds-home-fact-list')
    #                 print(house_details)
    # 
    # 
    #                 # ----------------------------------------------------------------------------------------------------------------------
    #                 # test_ds_home_fact_list = soup_house.find_all("span", {"class":"ds-home-fact-list"})
    #                 # ----------------------------------------------------------------------------------------------------------------------
    #                 type = ''
    #                 year = 0
    #                 heating = ''
    #                 cooling = ''
    #                 parking = 0
    #                 hoa = 0
    #                 prev_price = ''
    #                 # last_price_change = today_date
    #                 for span in factlabel_span:
    #                     label = span.text
    #                     labellist.append(label)
    #                 for span in factvalue_span:
    #                     value = span.text
    #                     valuelist.append(value)
    #                 for label_text in labellist:
    #                     i = labellist.index(label_text)
    #                     if 'type' in label_text.lower():
    #                         try:
    #                             type = valuelist[i].lower()
    #                         except ValueError:
    #                             type = ''
    #                     elif 'year built' in label_text.lower():
    #                         try:
    #                             year = int(valuelist[i])
    #                         except ValueError:
    #                             year = ''
    #                     elif 'heating' in label_text.lower():
    #                         try:
    #                             heating = valuelist[i].lower()
    #                         except ValueError:
    #                             heating = ''
    #                     elif 'cooling' in label_text.lower():
    #                         try:
    #                             cooling = valuelist[i].lower()
    #                         except ValueError:
    #                             cooling = ''
    #                     elif 'parking' in label_text.lower():
    #                         parking= valuelist[i]
    #                         try:
    #                             parking = int(''.join(j for j in parking if j.isdigit()))
    #                         except ValueError:
    #                             parking = valuelist[i]
    #                     elif 'hoa' in label_text.lower():
    #                         hoa = valuelist[i]
    #                         try:
    #                             hoa = int(''.join(j for j in hoa if j.isdigit()))
    #                         except ValueError:
    #                             hoa = valuelist[i]
    #             #     cursor.execute(sql, (new_price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, house_url, last_price_change, prev_price))
    #             # con.commit()
    #             # cursor_new.execute(sql_new, (new_price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, house_url, last_price_change, prev_price))
    #             # con_new.commit()
    #         next_pg = soup.find("a", attrs={"title": "Next page"})['href']

# url ='https://www.zillow.com/homes/gainesville_rb/'



extract_and_store_data()
