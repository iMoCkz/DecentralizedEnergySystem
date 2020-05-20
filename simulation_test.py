import csv

with open("CSVExport.csv") as fp:
    reader = csv.reader(fp, delimiter=";")
    # next(reader, None)  # skip the headers
    data_read = [row for row in reader]

print(data_read)