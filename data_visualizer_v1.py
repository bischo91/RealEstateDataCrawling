from pandas import DataFrame
import sqlite3
from tkinter import *
import tkinter as tk
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from tkcalendar import DateEntry
import numpy as np

def append_data(data_date):
    # Creates a table in SQL if data exist.
    # Append data in string format after processing the data.
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
        # Create a new table in SQL
        cursor.execute("select name from sqlite_master where type='table' and name ='"
                    + table_name + "'")
        cursor.execute("select * from " + table_name)
        rows = cursor.fetchall()
        price = [int(row[0]) for row in rows]
        pricepersqft = []
        # Combine each parameter into a list of the parameter for all properties from the list of parameters of one property.
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
            # Adding general location from the address.
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
        # Delete if:
        # -Price or Price/sqft is 0.
        # -Property type is 'lot'.
        # -Number of bedroom is 0.
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
        return price, pricepersqft, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price, location
    else:
        return [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

def trend(start_date, end_date):
    # Append all data within the specified date range into a list for each parameter
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
        date_list.append(data_date)
        price_list.append(price)
        pricepersqft_list.append(pricepersqft)
        bds_list.append(bds)
        ba_list.append(ba)
        sqft_list.append(sqft)
        acres_list.append(acres)
        est_list.append(est)
        property_list.append(property)
        type_list.append(type)
        year_list.append(year)
        heating_list.append(heating)
        cooling_list.append(cooling)
        parking_list.append(parking)
        hoa_list.append(hoa)
        link_list.append(link)
        updated_on_list.append(updated_on)
        last_price_list.append(last_price)
        location_list.append(location)
    return price_list, pricepersqscrapa_list, sqft_list, acres_list, \
            est_list, property_list, type_list, year_list, heating_list, cooling_list, \
            parking_list, hoa_list, link_list, updated_on_list, last_price_list, \
            location_list, date_list

def update_graph():
    # Update graph when radio button is changed for both X and Y axes,
    # or when graph type is toggled (bar/scatter)
    ax1.clear()
    ax1.set_xlabel(CX_sel.get())
    ax1.set_ylabel(CY_sel.get())
    if rad_sel.get().lower() == 'date':
        # For date is selected
        if CY_sel.get() == 'Price':
            y_data = price
        elif CY_sel.get() == 'Price/sqft':
            y_data = pricepersqft
        if CX_sel.get() == 'bds':
            x_data = bds
        elif CX_sel.get() == 'ba':
            x_data = ba
        elif CX_sel.get() == 'location':
            x_data = location
        elif CX_sel.get() == 'sqft':
            x_data = sqft
        if rad_graph_type.get() == 'scatter':
            ax1.scatter(x_data, y_data)
        elif rad_graph_type.get() == 'bar':
            if x_data !=[]:
                df1 = DataFrame(dataset, columns = ['Price', 'Price/sqft', 'bds', 'ba', 'sqft', 'location'])
                df1_mean = df1[[CY_sel.get(), CX_sel.get()]].groupby(CX_sel.get()).mean()
                df1_std = df1[[CY_sel.get(), CX_sel.get()]].groupby(CX_sel.get()).apply(np.std)
                df1_mean.plot(kind='bar', legend=True, ax=ax1, yerr = df1_std, capsize = 10)
        if x_data == []:
            no_data_dates = str(sel_date.get_date())
            msg_content['text'] = 'No Data for: \n'+no_data_dates
        else:
            msg_content['text'] = ''
        figure1.suptitle(str(sel_date.get_date()))
        chart_type = FigureCanvasTkAgg(figure1, graph_frame)
        chart_type.get_tk_widget().grid(row = 1, column = 2)

    elif rad_sel.get().lower() == 'trend':
        # For trend is selected
        ax1.set_xlabel('Date')
        ax1.set_ylabel(CY_sel.get())
        no_data_dates = []
        no_data_index = []
        price_list, pricepersqft_list, bds_list, ba_list, sqft_list, \
        a,b,c,d,year_list,e,f,g,h,i,j,k,location_list,date_list = trend(from_date.get_date(), to_date.get_date())

        price_1_bds, price_2_bds, price_3_bds, price_4_bds, pricepersqft_1_bds, pricepersqft_2_bds, pricepersqft_3_bds, pricepersqft_4_bds, \
        price_NE, price_NW, price_SE, price_SW, pricepersqft_NE, pricepersqft_NW, pricepersqft_SE, pricepersqft_SW = ([] for i in range(16))
        date_list = []
        average_price = []
        for i in range(0, (to_date.get_date()-from_date.get_date()).days+1):
            dataset_trend = {'Price': price_list[i], 'Price/sqft': pricepersqft_list[i], 'bds': bds_list[i], 'ba': ba_list[i], 'sqft': sqft_list[i], 'location': location_list[i], 'date': len(price_list[i])*[from_date.get_date() + datetime.timedelta(days=i)]}
            df2 = DataFrame(dataset_trend, columns =['Price', 'Price/sqft', 'bds', 'ba', 'sqft', 'location', 'date'])
            df2_mean_by_bds = df2[['Price', 'Price/sqft', 'bds']].groupby('bds').mean()
            df2_mean_by_location = df2[['Price', 'Price/sqft', 'location']].groupby('location').mean()
            if len(df2_mean_by_bds.values) > 0:
                price_1_bds.append(df2_mean_by_bds.values[0][0])
                price_2_bds.append(df2_mean_by_bds.values[1][0])
                price_3_bds.append(df2_mean_by_bds.values[2][0])
                price_4_bds.append(df2_mean_by_bds.values[3][0])
                pricepersqft_1_bds.append(df2_mean_by_bds.values[0][1])
                pricepersqft_2_bds.append(df2_mean_by_bds.values[1][1])
                pricepersqft_3_bds.append(df2_mean_by_bds.values[2][1])
                pricepersqft_4_bds.append(df2_mean_by_bds.values[3][1])
                price_NE.append(df2_mean_by_location.values[0][0])
                price_NW.append(df2_mean_by_location.values[1][0])
                price_SE.append(df2_mean_by_location.values[2][0])
                price_SW.append(df2_mean_by_location.values[3][0])
                pricepersqft_NE.append(df2_mean_by_location.values[0][1])
                pricepersqft_NW.append(df2_mean_by_location.values[1][1])
                pricepersqft_SE.append(df2_mean_by_location.values[2][1])
                pricepersqft_SW.append(df2_mean_by_location.values[3][1])
            date_list.append((from_date.get_date() + datetime.timedelta(days=i)))

        average_price_list = []
        average_pricepersqft_list = []
        for i in range(0, len(price_list)):
            if len(price_list[i]) > 0:
                average_price = np.mean(price_list[i])
                average_price_list.append(average_price)
                average_pricepersqft = np.mean(pricepersqft_list[i])
                average_pricepersqft_list.append(average_pricepersqft)
            else:
                no_data_index.append(i)
                no_data_dates.append(date_list[i])
        date_list=np.delete(date_list, no_data_index).tolist()
        x_data = [i.strftime('%y/%m/%d') for i in date_list]
        if x_data != []:
            if CY_sel.get() == 'Price':
                y_data = average_price_list
                ax1.plot(x_data, y_data, label = 'All', color = 'Black', linewidth = '3')
                ax1.plot(x_data, price_NW, label = 'NW')
                ax1.plot(x_data, price_NE, label = 'NE')
                ax1.plot(x_data, price_SE, label = 'SE')
                ax1.plot(x_data, price_SW, label = 'SW')
            elif CY_sel.get() == 'Price/sqft':
                y_data = average_pricepersqft_list
                ax1.plot(x_data, y_data, label = 'All', color = 'Black', linewidth = '3')
                ax1.plot(x_data, pricepersqft_NW, label = 'NW')
                ax1.plot(x_data, pricepersqft_NE, label = 'NE')
                ax1.plot(x_data, pricepersqft_SE, label = 'SE')
                ax1.plot(x_data, pricepersqft_SW, label = 'SW')

            ax1.set_xticks(np.linspace(0, len(x_data)+5, 7))
            figure1.autofmt_xdate()
            ax1.legend(bbox_to_anchor = (1,1))
            figure1.suptitle(str(from_date.get_date())+' ~ '+str(to_date.get_date()))
            chart_type = FigureCanvasTkAgg(figure1, graph_frame)
            chart_type.get_tk_widget().grid(row = 1, column = 2)
        # Showing missing dates in the defined date range
        no_data_dates = ', '.join([str(elem) for elem in no_data_dates])
        msg_content['text'] = 'No Data for: \n'+no_data_dates

def update_date():
    # When date is changed, the graph is updated with the new date.
    global dataset, price, pricepersqft, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price, location
    date_selected = sel_date.get_date()
    price, pricepersqft, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price, location = append_data(date_selected)
    dataset = {'Price': price, 'Price/sqft': pricepersqft, 'bds': bds, 'ba': ba, 'sqft': sqft, 'location': location}
    update_graph()

def axis_update(rad_graph_type, CY_sel, CX_sel):
    # Disables to select 'bar' graph type and 'sqft' as x-axis at the same time
    CX[3].configure(state = NORMAL)
    rad_graph_bar.configure(state = NORMAL)
    if rad_graph_type.get() == 'bar':
        CX[3].configure(state = DISABLED)
    if CX_sel.get() == CX_text[3]:
        rad_graph_bar.configure(state = DISABLED)

def convert():
    # Graph converted depending on graph type.
    if rad_sel.get() == 'date':
        # temp_label['text'] = 'This is temporary spot for date'
        rad_graph_scatter.grid(row = 1, column = 0)
        rad_graph_bar.grid(row = 1, column = 1)
        sel_date.grid(row = 3, column = 0)
        date_msg.grid(row = 2, column = 0)
        from_msg.grid_forget()
        to_msg.grid_forget()
        from_date.grid_forget()
        to_date.grid_forget()
    elif rad_sel.get() == 'trend':
        from_date.grid(row = 3, column = 0)
        to_date.grid(row = 3, column = 1)
        from_msg.grid(row = 2, column = 0)
        to_msg.grid(row = 2, column = 1)
        sel_date.grid_forget()
        date_msg.grid_forget()
        rad_graph_scatter.grid_forget()
        rad_graph_bar.grid_forget()
        CX[0].configure(state = DISABLED)
        CX[1].configure(state = DISABLED)
        CX[2].configure(state = DISABLED)
        CX[3].configure(state = DISABLED)
    axis_update(rad_graph_type, CY_sel, CX_sel)
    update_graph()


# Window GUI
window = tk.Tk()
window.title("Real Estate Data")
window.geometry("960x600+10+10")
# Frame
xcheckbutton_frame = Frame(window)
ycheckbutton_frame = Frame(window)
option_frame = Frame(window)
plot_frame = Frame(window)
graph_frame = Frame(window)
# Grid
option_frame.grid(column = 2, row = 1)
ycheckbutton_frame.grid(column = 0, row = 1)
graph_frame.grid(column = 1, row = 1)
xcheckbutton_frame.grid(column = 1, row = 2)
plot_frame.grid(column = 2, row = 2)
# Message
msg_content = Label(window, text = '', width = 100, anchor = 'w')
msg_content.place(relx=0.1, rely=0.8)
# SQL Data Connection (Change to the path if not for an example)
con = sqlite3.connect("./real_estate_database_example.db")
cursor = con.cursor()
# Initialize Date
today_date = datetime.date.today()
start_date = today_date + datetime.timedelta(days = -7)
end_date = today_date
# Initialize Data using previous day data (days = -1)
price, pricepersqft, bds, ba, sqft, acres, est, property, type, year, heating, cooling, parking, hoa, link, updated_on, last_price, location = append_data(today_date)
dataset = {'Price': price, 'Price/sqft': pricepersqft, 'bds': bds, 'ba': ba, 'sqft': sqft, 'location': location}
# Plot
figure1 = plt.Figure(figsize=(8,5), dpi = 80)
ax1 = figure1.add_subplot(111)
figure1.suptitle(str(today_date))
ax1.scatter(bds, price)
chart_type = FigureCanvasTkAgg(figure1, graph_frame)
chart_type.get_tk_widget().grid(row = 1, column = 2)

# X/Y Axes Radiobutton
global rad_graph_type
global CX_sel
global CY_sel
CY_sel = StringVar()
CY_sel.set('Price')
CX_sel = StringVar()
CX_sel.set('bds')
CX = []
CY = []
CY_text = ['Price', 'Price/sqft']
CX_text = ['bds', 'ba', 'location', 'sqft']
ax1.set_xlabel(CX_sel.get())
ax1.set_ylabel(CY_sel.get())
for j in range(0,len(CY_text)):
    CY.append(Radiobutton(ycheckbutton_frame, text = CY_text[j],
     variable = CY_sel, value = CY_text[j], anchor = 'w', width = 15, height = 5, command = convert))
    CY[j].grid(row = j, column = 0)
for k in range(0, len(CX_text)):
    CX.append(Radiobutton(xcheckbutton_frame, text = CX_text[k],
    variable = CX_sel, value = CX_text[k], anchor = 'w', width = 15, height = 5, command = convert))
    CX[k].grid(row = 1, column = k)

# Data Representation Radiobutton
rad_sel = StringVar()
rad_sel.set('date')
rad_graph_type = StringVar()
rad_graph_type.set('scatter')
# Date Input
from_date = DateEntry(option_frame, width=10, background='grey',
                    foreground='white', borderwidth=2)
to_date = DateEntry(option_frame, width=10, background='grey',
                    foreground='white', borderwidth=2)
sel_date = DateEntry(option_frame, width=10, background='grey',
                    foreground='white', borderwidth=2)
date_msg = Label(option_frame, text = 'Select Date: ', width = 12, anchor = 'w')
from_msg = Label(option_frame, text = 'From: ', width = 12, anchor = 'w')
to_msg = Label(option_frame, text = 'To: ', width = 12, anchor = 'w')
rad_graph_scatter = Radiobutton(option_frame, text = 'Scatter',
                            variable=rad_graph_type, value = 'scatter', command = convert, width = 10, anchor = 'w')
rad_graph_bar = Radiobutton(option_frame, text = 'Bar',
                            variable=rad_graph_type, value = 'bar', command = convert, width = 10, anchor = 'w')
plot_btn = Button(plot_frame, text = 'Plot', command = update_date)
rad_graph_scatter.grid(row = 1, column = 0)
rad_graph_bar.grid(row = 1, column = 1)
date_msg.grid(row = 2, column = 0)
sel_date.grid(row = 3, column = 0)
plot_btn.grid(row = 4, column = 0)

lbl_option_date = Radiobutton(option_frame, text='Date',
                            variable=rad_sel, value = 'date', command = convert, width = 10, anchor = 'w')
lbl_option_date.grid(row = 0, column = 0)
lbl_option_trend = Radiobutton(option_frame, text='Trend',
                            variable=rad_sel, value = 'trend', command = convert, width = 10, anchor = 'w')
lbl_option_trend.deselect()
lbl_option_trend.grid(row = 0, column = 1)

window.mainloop()
