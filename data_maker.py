from random import randint
import csv

def create_data():
    val = 0 
    with open('roasting_data.csv', 'w',  newline = '') as csvfile:
            fieldnames = ['time', 'tmp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(180):
                if val <= 300:
                    val += randint(2, 10)
                if val >= 300:
                    val -= randint(5, 12)
                writer.writerow({'time': i, 'tmp': val})
            place_holder = 180
            for i in range(540):
                if val <= 405:
                    val += randint(2, 5)
                if val >= 405:
                    val -= randint(5, 12)
                writer.writerow({'time': i + place_holder, 'tmp': val})

    


create_data()

