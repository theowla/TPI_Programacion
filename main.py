import csv
from tabulate import tabulate

# -.-.-.-.-. HELPERS .-.-.-.-.-
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

def buscar_pais(busqueda: str) -> dict | None:
    busqueda = busqueda.lower().strip()
    return next((item for item in datos if busqueda in item["nombre"].lower()), None)


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

def filtrar_paises():
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

def estadisticas():
    ordenado = []
    ordenado = sorted(datos[1:], key=lambda x: int(x["poblacion"]))

    print(f"Menor población: {ordenado[0]['nombre']}\nMayor población: {ordenado[-1]['nombre']}")

    conteo_continentes = {}
    poblacion = 0
    superficie = 0

    for item in datos:
        if item["poblacion"] == "poblacion":
            continue
        poblacion += int(item["poblacion"])
        superficie += int(item["superficie"])
        continente = item["continente"]
        conteo_continentes[continente] = conteo_continentes.get(continente, 0) + 1

    promedio_poblacion = poblacion / len(datos)
    promedio_superficie = superficie / len(datos)
    print(f"Promedio de población: {promedio_poblacion:.0f}")
    print(f"Promedio de superficie: {promedio_superficie:.0f}")
    for item in conteo_continentes:
        print(f"{item} = {conteo_continentes[item]}")


# -.-.-.-.-. ACCIONES DEL MENÚ .-.-.-.-.-

def agregar_entrada():
    try:
        print("Ingrese los datos que se solicitan a continuación:")
        #nombre, poblacion, superficie, continente = input("> ").lower().split()
        nombre = input("Nombre > ").lower().strip().replace(" ", "")
        poblacion = input("Población > ").lower().strip()
        superficie = input("Superficie en km² > ").lower().strip()
        continente = input("Continente > ").lower().strip()

        if buscar_pais(nombre) is not None:
            raise ValueError("Ese país ya existe en la base de datos")
        if not nombre.isalpha() or not continente.isalpha():
            raise ValueError("Debe ser un nombre y continente valido")
        elif not poblacion.isdigit() or not superficie.isdigit():
            raise ValueError("La poblacion y superficie deben ser numero enteros")
        else:
            datos.append({"nombre":nombre, "poblacion":int(poblacion), "superficie":int(superficie),"continente":continente})
            guardar_cambios()
            print("Entrada agregada con éxito")
    except ValueError as e:
        print(f"Error: {e}")


def actualizar_pais():
    pais = buscar_pais(input("Pais a modificar > "))
    if pais is not None:
        nombre, poblacion, superficie, continente = pais.values()
        try:
            print("Ingrese los valores a modificar:")
            nueva_poblacion = input("Población > ").strip()
            nueva_superficie = input("Superficie > ").strip()
            if nueva_poblacion.isdigit() and nueva_superficie.isdigit():
                pais.update({"nombre":nombre,"poblacion":int(nueva_poblacion),"superficie":int(nueva_superficie),"continente":continente})
                guardar_cambios()
            else:
                raise ValueError("Error: Solo se admiten números.")
        except ValueError as e:
            print(e)
    else:
        print("Error: ese país no existe en la base de datos. Pruebe agregandolo.")

#
def main():
    while True:
        print("""\t---MENÚ---
        1) Agregar país
        2) Actualizar datos de país
        3) Buscar un país
        4) Filtrar países
        5) Mostrar países ordenados
        6) Ver estadísticas
        """)

        accion = input("Acción a realizar > ")

        match(accion):
            case '1':
                agregar_entrada()
            case '2':
                actualizar_pais()
            case '3':
                pass
            case '4':
                pass
            case '5':
                pass
            case '6':
                pass
            case _:
                pass


main()
