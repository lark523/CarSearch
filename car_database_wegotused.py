# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file
import pprint, ssl, re, sqlite3
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup


url = 'https://www.wegotused.com/pennsburg-inventory/'
#url = 'https://www.wegotused.com/hazleton-inventory/'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Create SQL Database
conn = sqlite3.connect('carinventorydb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS Make_Model;

CREATE TABLE Make_Model (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    mk_mdl    TEXT UNIQUE
);


CREATE TABLE Cars (
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    sku             TEXT UNIQUE,
    make_model_id   INTEGER,
    year            INTEGER,
    location        INTEGER,
    yard_date       INTEGER

);
''')


html = urllib.request.urlopen(url, context=ctx).read()
print("Retrieving...", url)
soup = BeautifulSoup(html, 'html.parser')

car_dict= {}
Car_list = []
Categories = ['SKU', 'Year', 'Make', 'Model', 'Color', 'Vehicle Row', 'Yard Date', 'Last Update', 'Vin']
tr_tags = soup.find_all('tr')
#print(tr_tags)


for tags in tr_tags:
    td_tags = tags.find_all('td')
    #print(td_tags)
    count = 0
    for tag in td_tags:
        car_dict[Categories[count]] = tag.get_text()
        #print(tag.get_text())
        count +=1
    #print(car_dict)
    #print(car_dict.keys())

    #temp_make = car_dict['Make']
    #temp_model = car_dict['Model']
    temp_make_model = car_dict['Make'] + ' ' + car_dict['Model']
    temp_year = car_dict['Year']
    temp_SKU = car_dict['SKU']
    temp_Row = car_dict['Vehicle Row']
    temp_date = car_dict['Yard Date']

    cur.execute('''INSERT OR IGNORE INTO Make_Model (mk_mdl) VALUES ( ? )''', (temp_make_model, ))
    cur.execute('SELECT id FROM Make_Model WHERE mk_mdl = ? ', (temp_make_model, ))
    make_model_id = cur.fetchone()[0]


    cur.execute('''INSERT OR REPLACE INTO Cars (sku, make_model_id, year, location, yard_date)
    VALUES (?, ?, ?, ?, ?)''', (temp_SKU, make_model_id, temp_year, temp_Row, temp_date) )

conn.commit()
print("Data retrieved from ", url)

#print("Creating database table...")
#site_table = cur.execute(''' SELECT Cars.sku, Make.name, Model.name, CarYear.yr, CarRow.loc
#FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow ON Cars.make_id = Make.id
#and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
#Cars.carrow_id = CarRow.id ORDER BY Cars.sku''')

#for item in site_table:
#print(cur.fetchone())
