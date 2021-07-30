from pandas import DataFrame
import sqlite3
from tkinter import *
import tkinter as tk
import datetime
# from datetime import strptime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from tkcalendar import DateEntry
import numpy as np
import pandas as pd
import itertools

def append_data(data_date):
    year = str(data_date.year)
    month = str('%02d' %data_date.month)
    date = str('%02d' %data_date.day)
    if len(month) == 1:
        month = '0' + month
    if len(date) == 1:
        date = '0' + date
    table_name = "real_estate_" + year + month + date
    cursor.execute(" select count(name) from sqlite_master where type = 'table' and name = '" + table_name + "'")
    if cursor.fetchone()[0] == 1:
        cursor.execute("select name from sqlite_master where type='table' and name ='"
                    + table_name + "'")
        cursor.execute("select * from " + table_name)
        rows = cursor.fetchall()
        price = [int(row[0]) for row in rows]
        pricepersqft = []
        for row in rows:
            try:
                pricepersqft.append(int(row[0])/float(row[3]))
            except ZeroDivisionError:
                pricepersqft.append(0)
        bds = [int(row[1]) for row in rows]
        ba = [float(row[2]) for row in rows]
        sqft = [float(row[3]) for row in rows]
        acres = [row[4] for row in rows]
        est = [row[5] for row in rows]
        property = [row[6] for row in rows]
        type = [row[7] for row in rows]
        year = [row[8] for row in rows]
        heating = [row[9] for row in rows]
        cooling = [row[10] for row in rows]
        parking = [row[11] for row in rows]
        hoa = [row[12] for row in rows]
        link = [row[13] for row in rows]
        updated_on = [row[14] for row in rows]
        last_price = [row[15] for row in rows]
        location = []
        for element in link:
            # if '-NW-' or '/NW-' in element.upper():
            if '-NW-' in element.upper() or '/NW-' in element.upper():
                location.append('NW')
            elif '-SW-' in element.upper() or '/SW-' in element.upper():
                location.append('SW')
            elif '-NE-' in element.upper() or '/NE-' in element.upper():
                location.append('NE')
            elif '-SE-' in element.upper() or '/SE-' in element.upper():
                location.append('SE')
            else:
                location.append('Unknown')
        # Data Filtration

        while 0 in price:
            j = price.index(0)
            del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
        while 0 in pricepersqft:
            j = pricepersqft.index(0)
            del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
        while 'lot' in property:
            j = property.index('lot')
            del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
        while 0 in bds:
            j = bds.index(0)
            del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], year[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
        for j in range(0, len(acres)):
            if acres[j]>0:
                del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], year[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
        return price, pricepersqft, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price, location
    else:
        return [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

def append_all_data(start_date, end_date):
    price_list = []
    pricepersqft_list = []
    bds_list = []
    ba_list = []
    sqft_list = []
    acres_list = []
    est_list = []
    property_list = []
    type_list = []
    year_list = []
    heating_list = []
    cooling_list = []
    parking_list = []
    hoa_list = []
    link_list = []
    updated_on_list = []
    last_price_list = []
    location_list = []
    date_list = []
    for i in range(0, (end_date-start_date).days+1):
            data_date =start_date + datetime.timedelta(i)
            price, pricepersqft, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price, location = append_data(data_date)
            # date_list.append(data_date)
            price_list.append(price)
            pricepersqft_list.append(pricepersqft)
            bds_list.append(bds)
            ba_list.append(ba)
            sqft_list.append(sqft)
            # acres_list.append(acres)
            # est_list.append(est)
            # property_list.append(property)
            # type_list.append(type)
            year_list.append(year)
            # heating_list.append(heating)
            # cooling_list.append(cooling)
            # parking_list.append(parking)
            # hoa_list.append(hoa)
            link_list.append(link)
            updated_on_list.append(updated_on)
            # last_price_list.append(last_price)
            location_list.append(location)
    return price_list, pricepersqft_list, bds_list, ba_list, sqft_list, \
            link_list, updated_on_list, location_list

def create_X_matrix(bds, ba, sqft):
    sqft = (np.array(sqft)/1000).tolist()
    x0 = np.ones(len(price))
    X = np.transpose(np.array([x0, sqft, bds, ba]))
    return X

def normal_equation(X, price):
    Y = np.transpose(np.array(price))

    inv_XtX = np.linalg.inv(np.transpose(X).dot(X))
    theta = (inv_XtX.dot(np.transpose(X))).dot(Y)
    return theta

def price_pred(theta, X):
    h = np.dot(theta, X)
    return h

def cost_function(theta, X, price):
    m = len(price)
    print(m)
    Y = np.transpose(np.array(price))
    sum_J = 0
    for i in range(0, m):
        h = price_pred(theta,X[i])
        diff = (h-Y[i])**2
        sum_J += diff
    print(sum_J)
    J = (1/(2*m))*sum_J
    return J

con = sqlite3.connect("D:/Database/real_estate_database.db")
cursor = con.cursor()
# Initialize Date
today_date = datetime.date.today()
start_date = today_date + datetime.timedelta(days = -1)
end_date = today_date
# Initialize Data using previous day data (days = -1)
database = append_all_data(start_date, end_date)
data = []

for i in range(0, len(database)):
    data.append(list(itertools.chain(*database[i])))

df = pd.DataFrame(data).T
df.columns = ['price', 'Price/sqft', 'bds', 'ba', 'sqft', 'link', 'date', 'location']
pd.set_option('display.max_rows', 3000)
# print(df)

price = data[0]
bds = data[2]
ba = data[3]
sqft = data[4]

# shorten data length for test



X = create_X_matrix(bds,ba,sqft)
theta = normal_equation(X, price)





print(cost_function(theta, X, price))

price_pred_list=[]
for i in range(0, len(price)):
    price_pred_list.append(price_pred(theta,X[i]))

df.insert(0, "pred", price_pred_list, True)
df["pred"] = df["pred"].astype('int64')
print(df)

# print(cost_function(theta, create_X_matrix(bds,ba,sqft), price))


# price_pred = A[0]*1 + A[1]*2.426 + A[2]*4 + A[3]*2

# print(price_pred)
# print(theta)

# rows = ['price', 'pricepersqft', 'bds', 'ba', 'sqft', \
# 'acres', 'est', 'property', 'type', 'year', 'heating', 'cooling', 'parking', 'hoa', \
# 'link', 'updated_on', 'last_price', 'location']

# SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_name';
# cursor.execute(" select count(name) from sqlite_master where type = 'table' and name = '" + table_name + "'")
# if cursor.fetchone()[0] == 1:
    # cursor.execute("select name from sqlite_master where type='table' and name ='"
                # + table_name + "'")
    # cursor.execute("select * from " + table_name)

# for i in range(0, (end_date-start_date).days+1):
#     data_date =start_date + datetime.timedelta(i)
#     try:
#         sql_query_temp = pd.read_sql_query(define_table_name(data_date), con)
#         sql_query.append(sql_query_temp)
#     except sqlite3.OperationalError:
#         print('No data for ' + data_date)
#
#
#
# try:
#     pricepersqft.append(int(row[0])/float(row[3]))
# except ZeroDivisionError:
#     pricepersqft.append(0)
# print(sql_query)



# table_name = "real_estate_" + year + month + date
        # cursor.execute("select name from sqlite_master where type='table' and name ='"
                    # + table_name + "'")
        # cursor.execute("select * from " + table_name)
        # rows = cursor.fetchall()

# # Initialize Date
# today_date = datetime.date.today()
# # Initialize Data using previous day data (days = -1)
# price, pricepersqft, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price, location = append_data(today_date)
# dataset = {'Price': price, 'Price/sqft': pricepersqft, 'bds': bds, 'ba': ba, 'sqft': sqft, 'location': location}
# # Plot
#
# # X/Y Axes Radiobutton
# global rad_graph_type
# global CX_sel
# global CY_sel
# CY_sel = StringVar()
# CY_sel.set('Price')
# CX_sel = StringVar()
# CX_sel.set('bds')
# CX = []
# CY = []
# CY_text = ['Price', 'Price/sqft']
# CX_text = ['bds', 'ba', 'location', 'sqft']
# ax1.set_xlabel(CX_sel.get())
# ax1.set_ylabel(CY_sel.get())
# for j in range(0,len(CY_text)):
#     CY.append(Radiobutton(ycheckbutton_frame, text = CY_text[j],
#      variable = CY_sel, value = CY_text[j], anchor = 'w', width = 15, height = 5, command = convert))
#     CY[j].grid(row = j, column = 0)
# for k in range(0, len(CX_text)):
#     CX.append(Radiobutton(xcheckbutton_frame, text = CX_text[k],
#     variable = CX_sel, value = CX_text[k], anchor = 'w', width = 15, height = 5, command = convert))
#     CX[k].grid(row = 1, column = k)
#
# # Data Representation Radiobutton
# rad_sel = StringVar()
# rad_sel.set('date')
# rad_graph_type = StringVar()
# rad_graph_type.set('scatter')
# # Date Input
# from_date = DateEntry(option_frame, width=10, background='grey',
#                     foreground='white', borderwidth=2)
# to_date = DateEntry(option_frame, width=10, background='grey',
#                     foreground='white', borderwidth=2)
# sel_date = DateEntry(option_frame, width=10, background='grey',
#                     foreground='white', borderwidth=2)
# date_msg = Label(option_frame, text = 'Select Date: ', width = 12, anchor = 'w')
# from_msg = Label(option_frame, text = 'From: ', width = 12, anchor = 'w')
# to_msg = Label(option_frame, text = 'To: ', width = 12, anchor = 'w')
# rad_graph_scatter = Radiobutton(option_frame, text = 'Scatter',
#                             variable=rad_graph_type, value = 'scatter', command = convert, width = 10, anchor = 'w')
# rad_graph_bar = Radiobutton(option_frame, text = 'Bar',
#                             variable=rad_graph_type, value = 'bar', command = convert, width = 10, anchor = 'w')
# plot_btn = Button(plot_frame, text = 'Plot', command = update_date)
# rad_graph_scatter.grid(row = 1, column = 0)
# rad_graph_bar.grid(row = 1, column = 1)
# date_msg.grid(row = 2, column = 0)
# sel_date.grid(row = 3, column = 0)
# plot_btn.grid(row = 4, column = 0)
#
# lbl_option_date = Radiobutton(option_frame, text='Date',
#                             variable=rad_sel, value = 'date', command = convert, width = 10, anchor = 'w')
# lbl_option_date.grid(row = 0, column = 0)
# lbl_option_trend = Radiobutton(option_frame, text='Trend',
#                             variable=rad_sel, value = 'trend', command = convert, width = 10, anchor = 'w')
# lbl_option_trend.deselect()
# lbl_option_trend.grid(row = 0, column = 1)
#
# window.mainloop()
