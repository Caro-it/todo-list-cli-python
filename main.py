# ============================================================
# 1. IMPORTS: traer herramientas que no vienen "sueltas"
# ============================================================
import csv          # módulo de la librería estándar para leer/escribir archivos CSV.
                    # Viene con Python, así que no hay que instalar nada (lo pide el enunciado).

# ============================================================
# 2. VARIABLES GLOBALES: datos que comparte todo el programa
# ============================================================
todos = []                 # lista vacía donde vivirán las tareas mientras el programa corre.
                           # Ejemplo después de agregar dos: ["Comprar cajas", "Revisar stock"]
stop = False               # "interruptor" del menú: mientras sea False, el menú se repite.
FILE_NAME = "todos.csv"    # nombre del archivo. En MAYÚSCULAS por convención = "constante,
                           # no la cambio". Si mañana se llama distinto, lo cambio solo aquí.


# ============================================================
# 3. FUNCIONES
# ============================================================

def get_todos():
    # Devuelve la lista. Es útil para que un test pueda "mirar" las tareas.
    global todos           # "global" = uso la variable de afuera, no creo una nueva aquí dentro
    return todos


def add_one_task(title):           # title = el texto que escribió el usuario
    global todos
    title = title.strip()          # strip() quita espacios al principio y al final: "  hola " -> "hola"
    if not title:                  # si quedó vacío ("" cuenta como False en Python)...
        print("La tarea no puede estar vacía.")
        return                     # ...salgo de la función sin agregar nada
    todos.append(title)            # append = añadir al FINAL de la lista
    print(f"Tarea agregada: {title}")   # f"..." = f-string: lo que va entre {} se reemplaza por su valor


def print_list():
    global todos
    if len(todos) == 0:            # len() = cuántos elementos tiene la lista
        print("No hay tareas pendientes.")
        return
    print("Tareas pendientes:")
    for position, task in enumerate(todos, start=1):
        # enumerate da DOS cosas en cada vuelta: un número y el elemento.
        # start=1 hace que cuente desde 1 (para humanos), no desde 0 (para Python).
        # Vuelta 1: position=1, task="Comprar cajas"
        # Vuelta 2: position=2, task="Revisar stock"
        print(f"{position}. {task}")


def delete_task(number_to_delete):    # llega como TEXTO, porque input() siempre devuelve texto
    global todos
    try:                               # "intenta esto..."
        position = int(number_to_delete)   # convierte "2" -> 2. Si es "hola", falla
    except (ValueError, TypeError):    # "...y si falla con este error, haz esto en vez de romperte"
        print("Debes indicar un número válido.")
        return
    if position < 1 or position > len(todos):   # ¿está fuera de rango? (ej: piden la 5 y hay 2)
        print(f"No existe la tarea {position}.")
        return
    removed = todos.pop(position - 1)
    # pop(i) saca el elemento en el índice i y lo DEVUELVE (por eso lo guardo en "removed").
    # El "- 1" traduce de humano a Python:  el usuario dice 1  ->  Python usa índice 0
    print(f"Tarea eliminada: {removed}")


def save_todos():
    global todos
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        # open(nombre, modo): "w" = write -> crea el archivo o lo SOBRESCRIBE entero.
        # newline=""        -> evita líneas en blanco de más en Windows.
        # encoding="utf-8"  -> para que tildes y ñ se guarden bien.
        # with ... as file  -> abre el archivo y lo CIERRA solo al terminar el bloque.
        writer = csv.writer(file)      # "escritor" de CSV conectado a ese archivo
        for task in todos:             # recorro cada tarea...
            writer.writerow([task])    # ...y escribo una FILA. Va entre [] porque una fila
                                       # es una lista de columnas (aquí, una sola columna).
    print(f"{len(todos)} tarea(s) guardada(s) en {FILE_NAME}")


def load_todos():
    global todos
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:   # "r" = read (leer)
            reader = csv.reader(file)   # "lector" de CSV: cada fila llega como lista, ej. ["Comprar cajas"]
            todos = [row[0] for row in reader if row and row[0].strip()]
            # Esto es una "list comprehension". Equivale a:
            #   nueva = []
            #   for row in reader:                    # por cada fila...
            #       if row and row[0].strip():        # ...si no está vacía...
            #           nueva.append(row[0])          # ...me quedo con su 1ª columna
            #   todos = nueva
            # Uso "=" (no append) para REEMPLAZAR la lista: si cargas dos veces no se duplica.
        print(f"{len(todos)} tarea(s) cargada(s) desde {FILE_NAME}")
    except FileNotFoundError:          # la 1ª vez el archivo aún no existe -> aviso y sigo
        print(f"No se encontró {FILE_NAME}. Empiezas con la lista vacía.")


# ============================================================
# 4. PROGRAMA PRINCIPAL: el menú
# ============================================================
if __name__ == "__main__":
    # Esta línea significa: "ejecuta lo de abajo SOLO si corro este archivo directamente"
    # (python main.py). Si otro archivo/test lo importa, el menú NO arranca,
    # pero las funciones sí quedan disponibles.

    while stop == False:               # bucle: repite todo esto mientras stop sea False
        print("""
    Elige una opción:
        1. Agregar una tarea
        2. Eliminar una tarea
        3. Mostrar la lista de tareas
        4. Guardar en todos.csv
        5. Cargar desde todos.csv
        6. Salir
    """)                               # triple comilla = texto de varias líneas
        response = input().strip()     # espera a que el usuario escriba y pulse Enter

        if response == "6":            # comparo con "6" TEXTO (input devuelve texto, no número)
            stop = True                # apago el interruptor -> el while termina -> programa termina
        elif response == "3":          # elif = "si no, y si..."
            print_list()
        elif response == "2":
            print_list()               # primero muestro la lista para que vea los números
            number_to_delete = input("¿Qué número de tarea quieres eliminar? ")
            delete_task(number_to_delete)
        elif response == "1":
            title = input("¿Qué tarea quieres agregar? ")
            add_one_task(title)
        elif response == "4":
            save_todos()
        elif response == "5":
            load_todos()
        else:                          # cualquier otra cosa que escriba
            print("Opción inválida: " + response)