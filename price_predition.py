import sqlite3
import pandas as pd
year = '2021'
month = '03'
date = '01'
table_name = "real_estate_" + year + month + date

con = sqlite3.connect("./real_estate_database_example.db")
cursor = con.cursor()

cursor.execute(" select count(name) from sqlite_master where type = 'table' and name = '" + table_name + "'")
# print(cursor.fetchone()[0])
temp=cursor.fetchone()[0]
if temp == 1:
    # cursor.execute("select name from sqlite_master where type='table' and name ='"
    #             + table_name + "'")
    cursor.execute("select * from " + table_name)
    rows = cursor.fetchall()
    df = pd.read_sql_query("select * from " + table_name, con)
    
    print(df)
#     price = [int(row[0]) for row in rows]
#     pricepersqft = []
#     for row in rows:
#         try:
#             pricepersqft.append(int(row[0])/float(row[3]))
#         except ZeroDivisionError:
#             pricepersqft.append(0)
#     bds = [int(row[1]) for row in rows]
#     ba = [float(row[2]) for row in rows]
#     sqft = [float(row[3]) for row in rows]
#     acres = [row[4] for row in rows]
#     est = [row[5] for row in rows]
#     property = [row[6] for row in rows]
#     type = [row[7] for row in rows]
#     year = [row[8] for row in rows]
#     heating = [row[9] for row in rows]
#     cooling = [row[10] for row in rows]
#     parking = [row[11] for row in rows]
#     hoa = [row[12] for row in rows]
#     link = [row[13] for row in rows]
#     updated_on = [row[14] for row in rows]
#     last_price = [row[15] for row in rows]
#     location = []
#     for element in link:
#         # if '-NW-' or '/NW-' in element.upper():
#         if '-NW-' in element.upper() or '/NW-' in element.upper():
#             location.append('NW')
#         elif '-SW-' in element.upper() or '/SW-' in element.upper():
#             location.append('SW')
#         elif '-NE-' in element.upper() or '/NE-' in element.upper():
#             location.append('NE')
#         elif '-SE-' in element.upper() or '/SE-' in element.upper():
#             location.append('SE')
#         else:
#             location.append('Unknown')
#     # Data Filtration
#     while 0 in price:
#         j = price.index(0)
#         del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
#     while 0 in pricepersqft:
#         j = pricepersqft.index(0)
#         del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
#     while 'lot' in property:
#         j = property.index('lot')
#         del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
#     while 0 in bds:
#         j = bds.index(0)
#         del price[j], pricepersqft[j], bds[j], ba[j], sqft[j], acres[j], est[j], property[j], type[j], year[j], heating[j], cooling[j], parking[j], hoa[j], link[j], updated_on[j], last_price[j], location[j]
