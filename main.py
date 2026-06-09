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


def mostrar_ordenado(modo: str, descendente: bool = True):
    ordenado = []
    match(modo):
        case 'n':
            ordenado = sorted(datos[1:], key=lambda x: x["nombre"].lower(),reverse=descendente)
        case 'p':
            ordenado = sorted(datos[1:], key=lambda x: int(x["poblacion"]),reverse=descendente)
        case 's':
            ordenado = sorted(datos[1:], key=lambda x: int(x["superficie"]),reverse=descendente)

    ordenado.insert(0,{"nombre":"nombre", "poblacion":"poblacion", "superficie":"superficie","continente":"continente"})
    mostrar_datos(ordenado)

def filtrar_pais():
    opcion = input("opcion de filtrado (continente, rango_poblacion, rango_superficie): ")
    if opcion == "continente":
        continentes = ["asia", "américa", "europa", "africa"]
        continente = input("continente: ").lower().strip()
        if continente in continentes:
            filtrado = []
            for item in datos:
                if item["continente"].lower().strip() == continente:
                    filtrado.append(item)

            mostrar_datos(filtrado)
        else:
            print("este continente no existe.")
    elif opcion == "rango_poblacion":
        cant_1, cant_2 = input("rango de poblacion (max min): ").split()
        filtrado = []
        for item in datos:
            if item["poblacion"] <= cant_1 and item["poblacion"] >= cant_2:
                filtrado.append(item)

        mostrar_datos(filtrado)
    elif opcion == "rango_superficie":
        cant_1, cant_2 = input("rango de superficie (max min): ").split()
        filtrado = []
        for item in datos:
            if item["superficie"] <= cant_1 and item["superficie"] >= cant_2:
                filtrado.append(item)

        mostrar_datos(filtrado)
    else:
        print("opcion invalida")

#actualizar_pais()
mostrar_ordenado("s",False)

#agregar_entrada()
#mostrar_datos(datos)
