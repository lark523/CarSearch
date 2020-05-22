import sqlite3

def Yard_Search(make, model, yr_range):


    conn = sqlite3.connect('carinventorydb.sqlite')
    cur = conn.cursor()

    print("Let's search the inventory...")
    select_make = make
    select_model = model
    year_range = yr_range

    year_min, year_max = year_range.split('-')


    cur.execute(''' SELECT CARS.sku, Make_Model.mk_mdl, Cars.year, Cars.Location, Cars.Yard_date
    FROM Cars JOIN Make_Model ON Cars.make_model_id = Make_model.id
    WHERE Make_Model.mk_mdl LIKE ? AND Make_Model.mk_mdl LIKE ? and Cars.year BETWEEN ? and ? ''',
    (select_make+'%', '%'+ select_model+'%', year_min, year_max, ))


    results = cur.fetchall()
    no_cars = len(results)
    print(no_cars,"results found")
    return (no_cars,results)
