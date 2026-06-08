import csv
from tabulate import tabulate

columnas = ('nombre','poblacion','superficie','continente')

def mostrar_datos(datos: list[dict]):
    print(tabulate(datos,tablefmt='simple_outline'))

def cargar_dataset():
    with open('datos/dataset.csv', mode='r', encoding='utf-8') as archivo:
        return list(csv.DictReader(archivo,columnas))

datos = cargar_dataset()

def guardar_cambios():
    with open('datos/dataset.csv', mode='w', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo,columnas)
        writer.writerows(datos)

def agregar_entrada():
    try:
        nombres, poblacion, superficie, continente = input("Ingresar datos (nombre poblacion superficie continente): ").lower().split()

        if nombres.isalpha() and continente.isalpha():
            datos.append({"nombre":nombres, "poblacion":int(poblacion), "superficie":int(superficie),"continente":continente})
            print(datos)
        else:
            raise ValueError("Debe ser un nombre y continente valido")
        if poblacion.isdigit() and superficie.isdigit():
            print("a")
        else:
            raise ValueError("La poblacion y superficie deben ser numero enteros")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        guardar_cambios()

def buscar_pais(busqueda) -> None | dict:
    for item in datos:
        if item["nombre"].lower().strip() == busqueda.lower().strip():
            return item
    return None

def actualizar_pais():
    pais = buscar_pais(input("Pais a buscar > "))
    if pais is not None:
        nombre, poblacion, superficie, continente = pais.values()

        try:
            nueva_poblacion, nueva_superficie= input("Ingresar datos (poblacion superficie): ").lower().split()
            if nueva_poblacion.isdigit() and nueva_superficie.isdigit():
                pais.update({"nombre":nombre,"poblacion":int(nueva_poblacion),"superficie":int(nueva_superficie),"continente":continente})
                guardar_cambios()
            else:
                raise ValueError("Solo se admiten números.")
        except ValueError as e:
            print(e)


#actualizar_pais()
#

agregar_entrada()
#mostrar_datos(datos)
