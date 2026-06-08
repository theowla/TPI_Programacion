import csv
from tabulate import tabulate

columnas = ('nombre','poblacion','superficie','continente')

def mostrar_datos(datos: list[dict]):
    print(tabulate(datos,tablefmt='simple_outline'))

def cargar_dataset():
    with open('datos/dataset.csv', mode='r', encoding='utf-8') as archivo:
        return list(csv.DictReader(archivo,columnas))

datos = cargar_dataset()

def agregar_entrada():
    with open('datos/dataset.csv', mode='w', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo,columnas)
        try:
            nombres, poblacion, superficie, continente = input("Ingresar datos (nombre poblacion superficie continente): ").lower().split()

            if nombres.isalpha() and continente.isalpha():
                datos.append({"nombre":nombres, "poblacion":int(poblacion), "superficie":int(superficie),"continente":continente})
                print(datos)

            else:
                raise ValueError("Debe ser un nombre y continente valido")
            if poblacion.isdigit() and superficie.isdigit():
                print("a")
            raise ValueError("La poblacion y superficie deben ser numero enteros")
        except ValueError as e:
            print(f"Error: {e}")
        finally:
            writer.writerows(datos)

agregar_entrada()

mostrar_datos(datos)
