import csv
import numpy as np  # type: ignore
import shutil

mu = 45
sigma = 15

with open('./modified_data/hotel_booking_simple.csv', 'r', newline='', encoding='utf-8') as csvfile, \
        open('temp.csv', 'w', newline='', encoding='utf-8') as temp_csvfile:

    # create reader and writer
    csvreader = csv.reader(csvfile)
    csvwriter = csv.writer(temp_csvfile)

    header = next(csvreader)
    header.append('age')
    csvwriter.writerow(header)

    for row in csvreader:
        age = int(np.random.normal(mu, sigma))
        age = max(min(age, 90), 17)
        row.append(age)
        csvwriter.writerow(row)

shutil.move('temp.csv', './modified_data/hotel_booking_simple(+age).csv')
