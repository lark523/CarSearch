import csv
import YardList

fhandle = input('Enter name of csv file: ')

#with open(fhandle) as carinfo:
car_sel = []
search_dict={}
search_results ={}
car_dict= {}
header = ['SKU', 'Make & Model','Year', 'Location', 'Yard Date']

with open(fhandle, 'r', newline='') as carinfo:
    with open('listresults.csv', 'w') as csv_file:
        #carfile = csv.writer(csv_file)
        carfile = csv.DictWriter(csv_file, header)
        carfile.writeheader()
        #carfile.writerows(header)
        reader = csv.reader(carinfo)
        count = 0
        for row in reader:
            #carfile.writerow(' '.join([str(item) for item in row]))
            for item in row:
                print(item)
                car_sel.append(item)
            quantity,search_results[count] = YardList.Yard_Search(car_sel[0], car_sel[1], car_sel[2])
            search_dict['SKU'] = car_sel[0]
            search_dict['Make & Model'] = car_sel[1]
            search_dict['Year'] = car_sel[2]
            search_dict['Yard Date'] = str(quantity)+' results found'
            carfile.writerow(search_dict)
            for res in search_results[count]:
                pos = 0
                for item in res:
                    car_dict[header[pos]] = item
                    pos +=1
                carfile.writerow(car_dict)
            #carfile.writerows(search_results[count])
            car_sel = []
            count += 1
