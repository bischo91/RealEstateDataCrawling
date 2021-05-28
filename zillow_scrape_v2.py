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
        driver.quit()
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
    saved_link = []
    saved_price= []
    saved_price_change = []
    today_date = str(datetime.date.today()).replace('-','')
    i = 0
    con = sqlite3.connect("D:/Database/real_estate_database.db")
    cursor = con.cursor()
    while not cursor.fetchone():
        i -= 1
        prev_date = str(datetime.date.today() + datetime.timedelta(days = i)).replace('-','')
        # prev_date = today_date # This
        table_name = "real_estate_" + prev_date
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")
    cursor.execute("select * from " + table_name)
    rows = cursor.fetchall()
    con_new = sqlite3.connect("D:/Database/real_estate_database.db")
    cursor_new = con_new.cursor()
    table_new = "real_estate_" + today_date

    cursor_new.execute("drop table if exists " + table_new) # create this
    cursor_new.execute("create table " + table_new + "(price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price)") # create this
    cursor_new.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_new + "'")
    sql_new = 'insert into ' + table_new + ' values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

    for row in rows:
        saved_price.append(row[0])
        saved_link.append(row[13])

    url ='https://www.zillow.com/homes/for_sale/gainesville-fl/'
    soup = url_opener(url)
    if soup != None:
        pages = []
        current_pg = 'invalid'
        # current_pg = '_p2'
        next_pg = ''
        while next_pg != current_pg:
            current_pg = next_pg
            if current_pg == '':
                print('Page 1')
            else:
                print('Page ' + str(''.join(filter(lambda i: i.isdigit(), current_pg))))
            url_pg = url + current_pg
            pages.append(url_pg)
            soup = url_opener(url_pg)
            for element in soup.find_all(class_='list-card'):
                house_url = element.find("a", class_='list-card-link')
                # print(house_url)
                try:
                    house_url = house_url['href']
                except TypeError:
                    print('URL not found')
                    print(house_rul)
                    break
                # house_url = house_url['href']
                price = element.select_one('.list-card-price').text
                price, est = price2data(price)
                new_price = price
                details = element.select_one('.list-card-details').text
                if house_url in saved_link:
                    j = saved_link.index(house_url)
                    last_price_change = ''
                    if int(new_price) == int(saved_price[j]):
                        prev_price = rows[j][15]
                        last_price_change = rows[j][14]
                    else:
                        # j=j+1
                        print("price updated for row id " + str(j+1))
                        prev_price = saved_price[j]
                        last_price_change = today_date
                    bds = rows[j][1]
                    ba = rows[j][2]
                    sqft = rows[j][3]
                    acres = rows[j][4]
                    est = rows[j][5]
                    property = rows[j][6]
                    type = rows[j][7]
                    year = rows[j][8]
                    heating = rows[j][9]
                    cooling = rows[j][10]
                    parking = rows[j][11]
                    hoa = rows[j][12]
                else:
                    bds, ba, sqft, acres, property = detailstr2data(details)
                    if est == True:
                        est = 'Estimate'
                    else:
                        est = ''
                    time.sleep(random.random()*10+random.random()*(random.random()*10))
                    try:
                        soup_house = url_opener(house_url)
                        soup_house = soup_house.find("ul", class_='ds-home-fact-list')
                        soup_house = soup_house.find_all("li")
                    except:
                        print('URL error for:')
                        print(house_url)
                        # break
                    type, year, heating, cooling, parking, hoa = '', '', '', '', '', 0
                    prev_price = ''
                    last_price_change = today_date
                    for house_detail in soup_house:
                        detail = house_detail.text
                        detail_list = detail.split(':')
                        if detail_list[0].lower() == 'type':
                            try:
                                type = detail_list[1]
                            except ValueError:
                                type = ''
                        elif detail_list[0].lower() == 'year built':
                            try:
                                year = int(detail_list[1])
                            except ValueError:
                                year = ''
                        elif detail_list[0].lower() == 'heating':
                            try:
                                heating = detail_list[1]
                            except ValueError:
                                heating = ''
                        elif detail_list[0].lower() == 'cooling':
                            try:
                                cooling = detail_list[1]
                            except ValueError:
                                cooling = ''
                        elif detail_list[0].lower() == 'parking':
                            try:
                                parking = detail_list[1]
                            except ValueError:
                                parking = ''
                        elif detail_list[0].lower() == 'hoa':
                            try:
                                hoa = detail_list[1].replace('$','').replace(',','')
                                hoa = hoa.lower()
                                if 'monthly' in hoa:
                                    hoa = float(hoa.replace('monthly',''))*12
                                elif 'quarterly' in hoa:
                                    hoa = float(hoa.replace('quarterly', ''))*4
                                elif 'annually' in hoa:
                                    hoa = float(hoa.replace('annually', ''))
                                elif 'semi-annually' in hoa:
                                    hoa = float(hoa.replace('semi-annually', ''))
                                elif 'yearly' in hoa:
                                    hoa = float(hoa.replace('yearly', ''))
                            except ValueError:
                                hoa = 0
                    print(house_url)
                cursor_new.execute(sql_new, (new_price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, house_url, last_price_change, prev_price))
                con_new.commit()  # MOVE THIS OUT OF ELSE:
                # cursor_new.execute(sql_new, (new_price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, house_url, last_price_change, prev_price))
                # con_new.commit()
            next_pg = soup.find("a", attrs={"title": "Next page"})['href']

        print(pages)
# url ='https://www.zillow.com/homes/gainesville_rb/'



extract_and_store_data()
