import csv
import random

with open('hotel_booking.csv', 'r', newline='', encoding='utf-8') as csvfile, \
     open('temp.csv', 'w', newline='', encoding='utf-8') as temp_csvfile:
    
    # create reader and writer
    csvreader = csv.reader(csvfile)
    csvwriter = csv.writer(temp_csvfile)
    
    header = next(csvreader)    
    header.append('age')
    csvwriter.writerow(header)
    
    for row in csvreader:
        age = random.randint(17, 90)
        row.append(age)
        csvwriter.writerow(row)
import os
os.rename('temp.csv', 'hotel_booking.csv')



