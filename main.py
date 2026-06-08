import csv
from tabulate import tabulate

columnas = ('nombre','poblacion','superficie','continente')

def mostrar_datos(datos: list[dict])

def cargar_paises():
    with open('datos/dataset.csv', mode='r', encoding='utf-8') as archivo:
        return list(csv.DictReader(archivo,columnas))

datos = cargar_paises()

print(tabulate(datos,tablefmt='simple_outline'))
