import csv
from tabulate import tabulate

# -.-.-.-.-. HELPERS .-.-.-.-.-
COLUMNAS = ('nombre','poblacion','superficie','continente')

def mostrar_datos(datos: list[dict]):
    print(tabulate(datos,tablefmt='simple_outline',headers='keys'))
    input("Enter para continuar...")

def cargar_dataset():
    with open('datos/dataset.csv', mode='r', encoding='utf-8') as archivo:
        return list(csv.DictReader(archivo))

datos = cargar_dataset()

def guardar_cambios():
    with open('datos/dataset.csv', mode='w', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, COLUMNAS)
        writer.writeheader()  # escribe el header
        writer.writerows(datos)

def buscar_pais(busqueda: str, parcial: bool = True) -> dict | None:
    busqueda = busqueda.lower().strip()
    if parcial:
        return next((item for item in datos if busqueda in item["nombre"].lower()), None)
    else:
        return next((item for item in datos if busqueda == item["nombre"].lower()), None)

# -.-.-.-.-. ACCIONES DEL MENÚ .-.-.-.-.-
def agregar_entrada():
    try:
        print("Ingrese los datos que se solicitan a continuación:")
        #nombre, poblacion, superficie, continente = input("> ").lower().split()
        nombre = input("Nombre > ").lower().strip().replace(" ", "")
        poblacion = input("Población > ").lower().strip()
        superficie = input("Superficie en km² > ").lower().strip()
        continente = input("Continente > ").lower().strip()

        if buscar_pais(nombre, False) is not None:
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

def filtrar_paises():
    print("Elija la opción de filtrado (c = Continente, p = Rango de población, s = Rango de superficie)")
    opcion = input("> ").strip().lower()

    try:
        if opcion == "c" or opcion == "continente":
            continentes = ["asia", "américa", "europa", "africa", "oceanía"]
            continente = input("Continente > ").lower().strip()
            if continente in continentes:
                filtrado = []
                for item in datos:
                    if item["continente"].lower().strip() == continente:
                        filtrado.append(item)
                mostrar_datos(filtrado)
            else:
                print("Error: ese continente no existe.")

        elif opcion == "p" or opcion == "poblacion":
            cant_1, cant_2 = input("Ingrese rango separado por espacios (min max) > ").split()
            filtrado = []
            for item in datos:
                if int(cant_1) <= int(item["poblacion"]) <= int(cant_2):
                    filtrado.append(item)
            mostrar_datos(filtrado)

        elif opcion == "s" or opcion == "superficie":
            cant_1, cant_2 = input("Ingrese rango separado por espacios (min max): ").split()
            filtrado = []
            for item in datos:
                if int(cant_1) <= int(item["superficie"]) <= int(cant_2):
                    filtrado.append(item)
            mostrar_datos(filtrado)
        else:
            print("Error: opcion inválida.")
    except ValueError as e:
        print(f"{e}")

def mostrar_ordenado():
    print("Elija la opción de orden (n = Nombre, p = Población, s = Superficie)")
    modo_orden = input("> ").strip().lower()
    print("Modo de Visualización (a = ascendente, d = desendente)")
    modo_visualizacion = input("> ").strip().lower()
    descendente = False if modo_visualizacion == 'a' else True
    ordenado = []
    match(modo_orden):
        case 'n':
            ordenado = sorted(datos[1:], key=lambda x: x["nombre"].lower(),reverse=descendente)
        case 'p':
            ordenado = sorted(datos[1:], key=lambda x: int(x["poblacion"]),reverse=descendente)
        case 's':
            ordenado = sorted(datos[1:], key=lambda x: int(x["superficie"]),reverse=descendente)
        case _:
            print("Error: esa opción no existe.")

    mostrar_datos(ordenado)

def estadisticas():
    lista_completa = []
    ordenado = []
    ordenado = sorted(datos[1:], key=lambda x: int(x["poblacion"]))
    #print(f"Menor población: {ordenado[0]['nombre']}\nMayor población: {ordenado[-1]['nombre']}")
    lista_completa.append({"Estadística": "País con menor población", "Valor": ordenado[0]['nombre']})
    lista_completa.append({"Estadística": "País con mayor población", "Valor": ordenado[-1]['nombre']})

    conteo_continentes = {}
    contador_poblacion = 0
    contador_superficie = 0

    for item in datos:
        contador_poblacion += int(item["poblacion"])
        contador_superficie += int(item["superficie"])
        continente = item["continente"]
        conteo_continentes[continente] = conteo_continentes.get(continente, 0) + 1

    promedio_poblacion = contador_poblacion / len(datos)
    promedio_superficie = contador_superficie / len(datos)
    #print(f"Promedio de población: {promedio_poblacion:.0f}")
    #print(f"Promedio de superficie: {promedio_superficie:.0f}")

    lista_completa.append({"Estadística": "Promedio de Población", "Valor": f"{promedio_poblacion:.0f}"})
    lista_completa.append({"Estadística": "Promedio de Superficie", "Valor": f"{promedio_superficie:.0f}"})

    for k, v in conteo_continentes.items():
        lista_completa.append({"Estadística": k, "Valor": v})

    mostrar_datos(lista_completa)


# -.-.-.-.-. MENÚ .-.-.-.-.-
def main():
    while True:
        print("""\n\t  ---MENÚ---
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
                busqueda = buscar_pais(input("País a buscar > "))
                if busqueda is not None:
                    mostrar_datos([busqueda])
                    #print(f"\n{tabulate([busqueda],headers='keys')}\n")
                else:
                    print("Error: ese país no existe en la base de datos.")
            case '4':
                filtrar_paises()
            case '5':
                mostrar_ordenado()
            case '6':
                estadisticas()
            case _:
                print("Error: esa opción no existe.")
main()
