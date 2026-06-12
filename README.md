# Trabajo Práctico Integrador — Programación I

Sistema de gestión de datos de países desarrollado en Python. Permite agregar, buscar, filtrar, ordenar y visualizar estadísticas de países a partir de un archivo CSV.

---

## Link de video explicativo
https://www.youtube.com/watch?v=U7EVM54hzIc&list=WL&index=1&t=9s

## Integrantes

| Nombre |
|--------|
| Facundo González | 
| Theo Wlasiczuk |

---

## Requisitos

- Python 3.10 o superior
- Librería `tabulate`

Instalar `tabulate` con el siguiente comando:

```bash
pip install tabulate
```

---

## Estructura del proyecto

```
TPI-Programacion/
├── datos/
│   └── dataset.csv
├── README.md
└── main.py
```

---

## Uso

```bash
python main.py
```

El programa presenta un menú interactivo en consola con las siguientes opciones:

```
       ---MENÚ---
     1) Agregar país
     2) Actualizar datos de país
     3) Buscar un país
     4) Filtrar países
     5) Mostrar países ordenados
     6) Ver estadísticas
```

---

## Funcionalidades

**Agregar país** — Pide nombre, población, superficie y continente del país a agregar. Valida que no existan campos vacíos ni países duplicados.

**Actualizar país** — Busca un país por nombre (permite coincidencia parcial) para modificar su población y superficie.

**Buscar país** — Búsqueda por nombre con coincidencia parcial o completa. Muestra los datos del país encontrado.

**Filtrar países** — Filtra por continente, rango de población o rango de superficie.

**Ordenar países** — Ordena por nombre, población o superficie en modo ascendente o descendente.

**Estadísticas** — Muestra país con mayor y menor población, promedios de población y superficie, y cantidad de países por continente.

---
