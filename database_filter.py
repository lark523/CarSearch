import sqlite3

conn = sqlite3.connect('carinventorydb.sqlite')
cur = conn.cursor()

print("Let's search the inventory...")
select_make = input("Please enter the make 'Ford': ")
select_model = input("Please enter the model 'Explorer': ")
year_range = input("Please enter the year-range '2000-2005': ")

if year_range != "": year_min, year_max = year_range.split('-')


if select_make == '' and select_model == '' and year_range =='':
    cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
    FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
    ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
    Cars.carrow_id = CarRow.id ''')
elif select_make == '':
    if select_model == '':
        cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
        FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
        ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
        Cars.carrow_id = CarRow.id WHERE CarYear.yr BETWEEN ? and ? ''',
         (year_min, year_max, ))
    elif year_range =='':
        cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
        FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
        ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
        Cars.carrow_id = CarRow.id WHERE MODEL.NAME = ? ''',
         (select_model.upper(), ))
    else:
        cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
        FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
        ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
        Cars.carrow_id = CarRow.id WHERE MODEL.NAME = ? and CarYear.yr BETWEEN ? and ? ''',
         (select_model.upper(), year_min, year_max, ))

elif select_model == '':
    if year_range == '':
        cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
        FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
        ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
        Cars.carrow_id = CarRow.id WHERE MAKE.name = ? ''',
        (select_make.upper(), ))
    else:
        cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
        FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
        ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
        Cars.carrow_id = CarRow.id WHERE MAKE.name = ? AND  CarYear.yr BETWEEN ? and ? ''',
        (select_make.upper(), year_min, year_max, ))

elif year_range == '':
    cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
    FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
    ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
    Cars.carrow_id = CarRow.id WHERE MAKE.name = ? AND MODEL.NAME = ? ''',
     (select_make.upper(), select_model.upper(), ))

else:
    cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
    FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
    ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
    Cars.carrow_id = CarRow.id WHERE MAKE.name = ? AND MODEL.NAME = ? and CarYear.yr BETWEEN ? and ? ''',
     (select_make.upper(), select_model.upper(), year_min, year_max, ))


results = cur.fetchall()
no_cars = len(results)

if no_cars == 0: print("No results found")
else:
    print(no_cars," matches found")
    for row in results:
        print(row)
#for r in results:
#    print(r)

#if cur.fetchone() is None:
    #print ("No results found.")
#else:
#print(dir(results))
