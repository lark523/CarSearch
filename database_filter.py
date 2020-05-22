import sqlite3

conn = sqlite3.connect('carinventorydb.sqlite')
cur = conn.cursor()

print("Let's search the inventory...")
select_make = input("Please enter the make 'Ford': ")
select_model = input("Please enter the model 'Explorer': ")
year_range = input("Please enter the year-range '2000-2005': ")

if year_range != "": year_min, year_max = year_range.split('-')


if select_make == '' and select_model == '' and year_range =='':
    cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
    FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id ''')
elif select_make == '':
    if select_model == '':
        cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
        FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id
        WHERE Cars.year BETWEEN ? AND ? ''',
         (year_min, year_max, ))
    elif year_range =='':
        cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
        FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id
        WHERE Make_Model.mk_mdl LIKE ?  ''',
         ('%'+ select_model+'%', ))
    else:
        cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
        FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id
        WHERE Make_Model.mk_mdl LIKE ? AND Cars.year BETWEEN ? AND ? ''',
         ('%'+ select_model+'%', year_min, year_max, ))

elif select_model == '':
    if year_range == '':
        cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
        FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id
        WHERE Make_Model.mk_mdl LIKE ? ''',
        (select_make+'%', ))
    else:
        cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
        FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id
        WHERE Make_Model.mk_mdl LIKE ? AND Cars.year BETWEEN ? AND ? ''',
        (select_make +'%', year_min, year_max, ))

elif year_range == '':
    cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
    FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id
    WHERE Make_Model.mk_mdl LIKE ? AND Make_Model.mk_mdl LIKE ? ''',
     (select_make +'%', '%'+ select_model + '%', ))

else:
    cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
    FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id
    WHERE Make_Model.mk_mdl LIKE ? AND Make_Model.mk_mdl LIKE ? and Cars.year BETWEEN ? AND ? ''',
     (select_make + '%', '%' + select_model + '%', year_min, year_max, ))


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
