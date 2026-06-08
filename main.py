import csv

with open('datos/dataset.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        print(fila['nombre']) 