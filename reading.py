import csv

with open('roasting_data.csv',  newline = '') as csvfile:
    reader = csv.DictReader(csvfile)
    data = {}
    for row in reader:
        data[int(row['time'])] = int(row['tmp'])
    
    for i in data.keys():
        print("%d %d" %(i, data[i]))
