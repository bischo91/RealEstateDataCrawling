import os
import time
import sys
import numpy as np
import pandas as pd
import regex as re
import time
import sqlite3
from datetime import date
from lxml.html import fromstring


con = sqlite3.connect("C:/CS/python_ruby/finance/real_estate/real_estate_database.db")
cursor = con.cursor()
table_name = "real_estate_database"
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")
# if cursor.fetchall() != []:
    # print('table exists')
    # cursor.execute("select * from " + table_name)
    # rows = cursor.fetchall()
    # for row in rows:
#         saved_link.append(row[13])
#         saved_price.append(row[0])
# else:
# cursor.execute("create table " + table_name + "(price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price)")

con_1 = sqlite3.connect("C:/CS/python_ruby/finance/real_estate/real_estate_database.db")
cursor_1 = con_1.cursor()
table_name_1 = "real_estate_database"
cursor_1.execute("select * from " + table_name_1)

rows = cursor_1.fetchall()
# price, bds, ba, sqft, acres, est, property, type = [], [], [], [], [], [], [], []
# year, heating, cooling, parking, hoa, house_url, updated_on, last_price = [], [], [], [], [], [], [], []
# all_data = [price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, house_url, updated_on, last_price]
print(rows)
print(rows[800][6])
sql = 'insert into ' + table_name + ' values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

for row in rows:
    updated_on = ''
    last_price = ''
    # for i in range(0,len(all_data)-2):
        # all_data[i].append(row[i])
    # cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], updated_on, last_price))

#     for i in range(0,len(row[0])):
#         price.append(row[i])

# con_1.commit()
# print(all_data)
# print(len(all_data[15]))
# print(price)
# print(bds)
# print(parking)
# print(link)
# print(len(all_data))
# cursor.execute(sql, (price, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, house_url, updated_on, last_price))
# cursor.execute(sql, (rows[0]))
# con.commit()
