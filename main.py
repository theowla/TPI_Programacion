# =====================================================
# Programación 1 - UTN
# Trabajo Práctico Integrador
# Alumnos:
#   Theo Wlasiczuk (Revision de codigo, funciones (1-3))
#   Facundo González (Versionado de codigo, funciones (4-6))
# =====================================================

import csv #libreria para mejor manejo de archivos CSV
from tabulate import tabulate #libreria para mejores tablas

# -.-.-.-.-. HELPERS .-.-.-.-.-

# Columnas del CSV en orden de escritura
COLUMNAS = ('nombre','poblacion','superficie','continente')
# Opciones válidas de continente (se usa para mostrar y para indexar)
CONTINENTES = ("África","América","Asia","Europa","Oceanía")

def mostrar_datos(datos: list[dict]): #funcion para mostrar datos en una tabla
    print(tabulate(datos,tablefmt='simple_outline',headers='keys'))
    input("Enter para continuar...")

def cargar_dataset() -> list[dict]: #funcion de apertura del archivo CSV
    with open('datos/dataset.csv', mode='r', encoding='utf-8') as archivo:
        return list(csv.DictReader(archivo)) #devolvemos una lista de diccionarios

# Variable global que almacena los datos en memoria durante la ejecución
datos = cargar_dataset()

def guardar_cambios() -> None: #funcion para guardar los cambios en el archivo
    with open('datos/dataset.csv', mode='w', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, COLUMNAS) #guardamos en archivo los header
        writer.writeheader()
        writer.writerows(datos) #guardamos los valores

def buscar_pais(busqueda: str, parcial: bool = True) -> dict | None: 
    # parcial=True busca coincidencia parcial, parcial=False requiere nombre exacto
    if not busqueda:
        return
    busqueda = busqueda.lower().strip() #estandarizamos la entrada del usuario
    if parcial:
        return next((item for item in datos if busqueda in item["nombre"].lower()), None) #busqueda parcial (in)
    else:
        return next((item for item in datos if busqueda == item["nombre"].lower()), None) #busqueda exacta (==)


# -.-.-.-.-. ACCIONES DEL MENÚ .-.-.-.-.-
def agregar_entrada():
    try:
        print("Ingrese los datos que se solicitan a continuación:")
        # Se eliminan espacios para evitar duplicados como "Nueva Zelanda" vs "NuevaZelanda"
        nombre = input("Nombre > ").strip().replace(" ", "") #pedimos el nombre y lo estandarizamos

        if not nombre.isalpha(): #evitamos texto vacio y numeros
            raise ValueError("Nombre de país inválido")
        if buscar_pais(nombre, False) is not None: #evitamos duplicados
            raise ValueError("Ese país ya existe en la base de datos")

        poblacion = input("Población > ").strip() #pedimos la poblacion y superficie y estandarizamos
        superficie = input("Superficie en km² > ").strip()

        if not poblacion.isdigit() or not superficie.isdigit(): #verificamos los valores
            raise ValueError("La poblacion y superficie deben ser numeros enteros.")

        print("Elija el continente:\n1-África\n2-América\n3-Asia\n4-Europa\n5-Oceanía ")
        continente_elegido = input("Opción (1-5) > ").strip() #pedimos una opcion y estandarizamos
        if not continente_elegido.isdigit() or int(continente_elegido) not in range(1,6): #verificamos la opcion
            raise ValueError("Opción de continente inválida")
        continente_elegido = int(continente_elegido) 
    except ValueError as e:
        print(f"Error: {e}")
    else:
        # El índice del continente elegido se mapea a su nombre en la tupla CONTINENTES
        datos.append({"nombre":nombre.title(), "poblacion":int(poblacion), "superficie":int(superficie),"continente":CONTINENTES[continente_elegido-1]})
        guardar_cambios()
        print("Entrada agregada con éxito")

def actualizar_pais():
    pais = buscar_pais(input("Pais a modificar > ")) #pedimos un pais y llamamos a la funcion buscar_pais()
    if pais is not None: #validamos
        nombre, poblacion, superficie, continente = pais.values() #guardamos sus datos en variables temporales
        try:
            print(f"Ingrese los valores a modificar de {nombre}:") 
            nueva_poblacion = input("Población > ").strip() #pedimos los valores a modificar y estandarizamos
            nueva_superficie = input("Superficie > ").strip()
            if nueva_poblacion.isdigit() and nueva_superficie.isdigit(): #validamos
                # pais es una referencia al dict original en la lista global, esta línea lo modifica directamente
                pais.update({"nombre":nombre,"poblacion":int(nueva_poblacion),"superficie":int(nueva_superficie),"continente":continente})
                print("País modificado con éxito.")
                guardar_cambios()
            else:
                raise ValueError("Error: Solo se admiten números.")
        except ValueError as e:
            print(e)
    else:
        print("Error: ese país no existe en la base de datos. Pruebe agregandolo.")

def filtrar_paises():
    print("Elija la opción de filtrado (c = Continente, p = Rango de población, s = Rango de superficie)")
    opcion = input("> ").strip().lower() #pedimos una opcion y estandarizamos

    try:
        if opcion == "c" or opcion == "continente": #validamos

            print("Elija el continente:\n1-África\n2-América\n3-Asia\n4-Europa\n5-Oceanía ")
            continente_elegido = input("Opción (1-5) > ").strip() #pedimos una opcion y estandarizamos
            if not continente_elegido.isdigit() or int(continente_elegido) not in range(1,6): #validamos
                raise ValueError("Opción de continente inválida")
            continente_elegido = int(continente_elegido)

            filtrado = []
            for item in datos: #recorremos la datos diccionario por diccionario y organizamos por continente
                if item["continente"] == CONTINENTES[continente_elegido-1]:
                    filtrado.append(item) #guardamos en una variable temporal
            mostrar_datos(filtrado)

        elif opcion == "p" or opcion == "poblacion":
            try:
                cant_1, cant_2 = input("Ingrese rango separado por espacios (min max) > ").split() #pedimos un rango y estandarizamos
            except:
                print("No hay suficientes datos")
                return
            if not cant_1.isdigit() or not cant_2.isdigit(): #validamos
                raise ValueError("Error: El rango debe contener dos números enteros.")
            filtrado = []
            for item in datos: #recorremos datos y verificamos que entre en el rango
                if int(cant_1) <= int(item["poblacion"]) <= int(cant_2):
                    filtrado.append(item)
            if not filtrado:
                print("No hay paises que cumplan con esas caracteristicas.")
            mostrar_datos(filtrado)

        elif opcion == "s" or opcion == "superficie":
            try:
                cant_1, cant_2 = input("Ingrese rango separado por espacios (min max): ").split() #pedimos un rango y estandarizamos
            except:
                print("No hay suficientes datos")
                return
            if not cant_1.isdigit() or not cant_2.isdigit(): #validamos
                raise ValueError("Error: El rango debe contener dos números enteros.")
            filtrado = []
            for item in datos: #recorremos datos y verificamos que entre en el rango
                if int(cant_1) <= int(item["superficie"]) <= int(cant_2):
                    filtrado.append(item)
            if not filtrado:
                print("No hay paises que cumplan con esas caracteristicas.")
            mostrar_datos(filtrado)
        else:
            print("Error: opcion inválida.")
    except ValueError as e:
        print(f"{e}")

def mostrar_ordenado():
    print("Elija la opción de orden (n = Nombre, p = Población, s = Superficie)")
    modo_orden = input("> ").strip().lower() #pedimos una opcion y estandarizamos
    print("Modo de Visualización (a = ascendente, d = desendente <- default)")
    modo_visualizacion = input("> ").strip().lower() #pedimos un modo de visualizacion y estandarizamos
    descendente = False if modo_visualizacion == 'a' else True
    ordenado = []
    #ordenamos con sorted() dependiendo de la opcion elegida
    match(modo_orden):
        case 'n':
            ordenado = sorted(datos, key=lambda x: x["nombre"].lower(),reverse=descendente)
        case 'p':
            ordenado = sorted(datos, key=lambda x: int(x["poblacion"]),reverse=descendente)
        case 's':
            ordenado = sorted(datos, key=lambda x: int(x["superficie"]),reverse=descendente)
        case _:
            print("Error: esa opción no existe.")

    if ordenado:
        mostrar_datos(ordenado)

def estadisticas():
    lista_completa = []
    ordenado = []
    ordenado = sorted(datos, key=lambda x: int(x["poblacion"])) #ordenamos con sorted y luego tomamos el primero y el ultimo de la lista
    lista_completa.append({"Estadística": "País con menor población", "Valor": ordenado[0]['nombre']})
    lista_completa.append({"Estadística": "País con mayor población", "Valor": ordenado[-1]['nombre']})

    # Se usa un dict para contar países por continente: {continente: cantidad}
    conteo_continentes = {}
    contador_poblacion = 0
    contador_superficie = 0

    for item in datos: #recorremos datos y sumamos sus datos para el promedio
        contador_poblacion += int(item["poblacion"])
        contador_superficie += int(item["superficie"])
        continente = item["continente"]
        # get(continente, 0) evita KeyError si el continente no fue visto antes
        conteo_continentes[continente] = conteo_continentes.get(continente, 0) + 1 #suma 1 al diccionario si ya existe

    promedio_poblacion = contador_poblacion / len(datos) #dividimos los datos por la cantidad de paises para el promedio
    promedio_superficie = contador_superficie / len(datos)

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
        7) salir del programa
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
            case '7':
                return
            case _:
                print("Error: esa opción no existe.")
main()
