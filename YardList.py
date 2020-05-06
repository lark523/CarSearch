import sqlite3

def Yard_Search(make, model, yr_range):


    conn = sqlite3.connect('carinventorydb.sqlite')
    cur = conn.cursor()

    print("Let's search the inventory...")
    select_make = make
    select_model = model
    year_range = yr_range

    year_min, year_max = year_range.split('-')


    cur.execute(''' SELECT CARS.sku, MAKE.NAME, Model.name, CarYear.yr, CarRow.loc
    FROM Cars JOIN Make JOIN Model JOIN CarYear JOIN CarRow
    ON Cars.make_id = Make.id and Cars.model_id = Model.id and Cars.caryear_id = CarYear.id and
    Cars.carrow_id = CarRow.id WHERE MAKE.name = ? AND MODEL.NAME = ? and CarYear.yr BETWEEN ? and ? ''',
    (select_make.upper(), select_model.upper(), year_min, year_max, ))


    results = cur.fetchall()
    no_cars = len(results)
    if no_cars == 0:
        print("No results found")
    return results

    #if no_cars == 0: print("No results found")
    #else:
        #csv.writer(no_cars," matches found")
        #for row in results:
            #csv.wrtier(row)
        #for row in results:
            #print(row)
