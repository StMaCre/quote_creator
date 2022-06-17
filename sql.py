import sqlite3
import csv

conn = sqlite3.connect('price1.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE "price1" (
    "Referencia" TEXT, 
    "Modelo" TEXT, 
    "PVP" REAL
)
''')

with open("price-list.csv") as csv_file: 
    csv_reader = csv.reader(csv_file, delimiter = ";")
    for row in csv_reader:
        print(row)
        Referencia = row[0]
        Modelo = row[1]
        PVP = row[2]
        cur.execute('''INSERT INTO price1(Referencia, Modelo, PVP) 
            VALUES (?,?,?)''', (Referencia, Modelo, PVP))
        conn.commit()