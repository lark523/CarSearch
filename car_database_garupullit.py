# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file
import pprint, ssl, re, sqlite3
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup


#url = 'https://garysupullit.com/inventory/'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Create SQL Database
conn = sqlite3.connect('carinventorydb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS Make;
DROP TABLE IF EXISTS Model;
DROP TABLE IF EXISTS CarYear;
DROP TABLE IF EXISTS CarRow;

CREATE TABLE Make (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Model (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE

);
CREATE TABLE CarYear (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    yr      INTEGER UNIQUE

);
CREATE TABLE CarRow (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    loc     INTEGER

);

CREATE TABLE Cars (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    sku         TEXT UNIQUE,
    make_id     INTEGER,
    model_id    INTEGER,
    caryear_id     INTEGER,
    carrow_id      INTEGER

);
''')


html = urllib.request.urlopen(url, context=ctx).read()
print("Retrieving...", url)
soup = BeautifulSoup(html, 'html.parser')

car_dict= {}
Car_list = []
Categories = ['SKU', 'Make', 'Model', 'Model Det', 'Year', 'Color', 'Body', 'Vehicle Row', 'Yard Date', 'link']
tr_tags = soup.find_all('tr')
#print(tr_tags)


for tags in tr_tags:
    td_tags = tags.find_all('td')
    if td_tags == []: continue
    #print(td_tags)
    #(print(len(td_tags)))
    count = 0
    for tag in td_tags:
        car_dict[Categories[count]] = tag.get_text()
        #print(Categories[count], tag.get_text())
        #print('____________')
        #print(type(Categories[count]))
        count +=1
    #print(car_dict)
    #print('************ \n' )
    #print(car_dict.keys())

    #if 'SKU' in car_dict: print("Valid")
    #if 'SKU' not in car_dict:
        #print("!!!!!!!!Warning!!!!")
        #print(car_dict)

    make = car_dict['Make']
    model = car_dict['Model']
    year = car_dict['Year']
    SKU = car_dict['SKU']
    Row = car_dict['Vehicle Row']

    cur.execute('''INSERT OR IGNORE INTO Make (name) VALUES ( ? )''', (make, ))
    cur.execute('SELECT id FROM Make WHERE name = ? ', (make, ))
    make_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Model (name) VALUES ( ? )''', (model, ))
    cur.execute('SELECT id FROM Model WHERE name = ? ', (model, ))
    model_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO CarYear (yr) VALUES ( ? )''', (year, ))
    cur.execute('SELECT id FROM CarYear WHERE yr = ? ', (year, ))
    caryear_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO CarRow (loc) VALUES ( ? )''', (Row, ))
    cur.execute('SELECT id FROM CarRow WHERE loc = ? ', (Row, ))
    carrow_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Cars (sku, make_id, model_id, caryear_id, carrow_id) VALUES (?, ?, ?, ?, ?)''',
        (SKU, make_id, model_id, caryear_id, carrow_id) )

conn.commit()

#print("Creating database table...")
#site_table = cur.execute(''' SELECT Cars.sku, Make.name, Model.name, CarYear.yr, CarRow.loc
#FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow ON Cars.make_id = Make.id
#and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
#Cars.carrow_id = CarRow.id ORDER BY Cars.sku''')

#for item in site_table:
#print(cur.fetchone())
