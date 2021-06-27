import sqlite3 #pymysql   cambio el modulo y el procedimiento es el mismo
import os
import platform
from tabulate import tabulate

def limpiar_pantalla ():
    """
    Ejecuta el comando correspondiente para limpiar pantalla.
    Funciona para linux y Windows.
    """
    if platform.system() == "Linux":
        os.system("clear")  #NUNCA ENTRA EN LA EXCEPCION
    else:
         os.system("cls")

############################################################################################################
def definirMenu(titulo,*args):
    """
    Imprime por pantalla un menu.
    Se le pasa un titulo como parametro y luego
    una cantidad n de strings que representarian las filas del menu
    
    Ej:
        definirMenu("TITULO PRINCIPAL","Crear Base de datos","Ingrese dato a una base")
        
        retorna:
        TITULO PRINCIPAL
    
    	0 - Crear Base de datos
    	1 - Ingrese dato a una base
        
    """
    print (f"\n    {titulo}\n")
    
    for num,fila in enumerate(args):      
          print(f"\t{num} - {fila}") 

############################################################################################################
def validar_entero(n):
    """
    Valida cualquier numero entero ingresado por teclado
    """
    while True:
        try:
            int(n)
            return n
        except ValueError:
            print("ADVERTENCIA ----> Ingrese un numero entero")
            n = input("Ingrese nuevamente el dato:")
############################################################################################################
def validar_float(n):
    """
    Valida cualquier numero float/entero ingresado por teclado.
    """
    copia = n
    while True:
        try:
            float(n)
            return n
        except ValueError:
            print("ADVERTENCIA ----> No deben ingresarse letras")
            n = input("Ingrese nuevamente el dato:")
############################################################################################################

def validar_opcion(opc):
    """
    Valida el ingreso correcto de "1" u "2" ingresado por teclado
    """
    while True:
        if opc == "1":

            return opc
        elif opc == "2":
            return opc
        else:
            print("ADVERTENCIA ----> No ingresaste una opcion correcta")
            opc = input("Ingrese Nuevamente la opcion (1:SI  2=NO): ")
############################################################################################################
def validar_nom_arch(n,arch):
    """
    Función auxiliar de insertar_base()
    Verifica que exista el nombre del archivo ingresado.
    """
    flag = 0
    while True:
        if n in arch:
            return n,flag
        else:
            flag = 1 #cambio el valor del flag para que impacte en la funcion insertar_base
            return n,flag
############################################################################################################
def lista_archivos(lista):
    """
    Imprime por pantalla los archivos en una ubicacion especifica.

    Requiere la biblioteca os
    EJ:
        ruta = os.getcwd()
        lista = os.listdir(ruta)
    """
    print("ARCHIVOS DISPONIBLES DISPONIBLES:\n")
    for i in lista:
        print("__",i)
    print()
############################################################################################################
def guardar (n):
    """
    Guarda y cierra un archivo SQL
    """
    n.commit()
    n.close()
############################################################################################################
def crear_base(NAME):
    """
    CONECTA CON SQL
    ###QUERY: inserta una fila en la base de datos

    FUNCIONES AUXILIARES
    limpiar_pantalla()
    guardar(n)

    BIBLIOTECAS:
    os,sqlite3(o sus variantes)

    """
    ext = ".db" #PARA VALIDAR LA EXTENSION Y CREAR LA BASE DE DATOS
    if ext in NAME:
        try:

            conn = sqlite3.connect(NAME) #Conecta con el nombre de la base de datos
            cursor = conn.cursor() #defino el cursor para armar las columnas
            #conectar(NAME)
            cursor.execute("CREATE TABLE productos (id INT, nombre TEXT, precio FLOAT)")#SQL
            guardar (conn)
            print(">>>  Base de datos Creada  <<<")
            print(" PRESIONE UNA TECLA PARA CONTINUAR ...")
            input("")
            limpiar_pantalla()#cls para windows

        except sqlite3.OperationalError:
            print("ADVERTENCIA ----> Hubo un error en la consulta")
            input("PRESIONE UNA TECLA PARA CONTINUAR ...")

    else:
        print('ADVERTENCIA ----> Debe ingresar el nombre con la extension ".db"')
        input("PRESIONE UNA TECLA PARA CONTINUAR ...")
############################################################################################################
def insertar_base (n,arch):
    """
    CONECTA CON SQL
    ###QUERY: inserta una fila en la base de datos

    FUNCIONES AUXILIARES
    limpiar_pantalla()
    guardar(n)
    validar_entero()
    validar_opcion(opcion)

    BIBLIOTECAS:
    os,sqlite3(o sus variantes)

    """
    resultado = validar_nom_arch(n,arch)
    if resultado[1] != 1: # VALOR DEL FLAG
        while True:
            conn = sqlite3.connect(n)
            cursor = conn.cursor()
            id = input ("Ingrese ID: ")
            id = int(validar_entero(id))
            producto = input ("Ingrese nombre del producto: ")
            precio = input ("Ingrese precio: ")
            precio = float(validar_float(precio))

            cursor.execute("INSERT INTO productos VALUES (?,?,?)",(id,producto,precio)) #SQL
            guardar(conn)
            print(">>>  Datos guardados exitosamente <<<")
            opcion = input(f"¿Desea ingresar un nuevo dato a {n} ? (1=SI 2=NO)  ")
            opcion = validar_opcion(opcion)
            if opcion == "2":
                break
    else:
        print("ADVERTENCIA ----> La tabla NO existe")
        input("PRESIONE UNA TECLA PARA CONTINUAR ...")
############################################################################################################
def ver_base (n,arch):
    """
    CONECTA CON SQL
    ###QUERY: Muestro la base de datos por pantalla

    FUNCIONES AUXILIARES
    limpiar_pantalla()
    guardar(n)

    bibliotecas:
    os, tabulate,sqlite3(o sus variantes)

    """
    resultado = validar_nom_arch(n,arch)
    if resultado[1] != 1: # VALOR DEL FLAG
        aux_list = n.split(".")

        nombre_base = aux_list[0]
        print (nombre_base)
        conn = sqlite3.connect(n)
        cursor = conn.cursor()
        ###QUERY: Muestro la base de datos por pantalla
        cursor.execute("SELECT * FROM productos ")#SQL
        datos = cursor.fetchall() # ACA ESTA LA TUPLA DE TUPLAS
        guardar(conn)
        limpiar_pantalla()
        print("---------------------------------------------------------------------")
        print(f"BASE DE DATOS ----> {n}")
        headers = ["ID","PRODUCTO","PRECIO"]
        print(tabulate(datos,headers,tablefmt = "fancy_grid" ))
        print("\n---------------------------------------------------------------------")
        input("PRESIONE UNA TECLA PARA CONTINUAR ...")
    else:
        print("ADVERTENCIA ----> La tabla NO existe")
        input("PRESIONE UNA TECLA PARA CONTINUAR ...")

############################################################################################################

def menu():
    """
    Funcion de alto nivel que muestra el menu principal
    
    """       

    while True:
    
        ruta = os.getcwd()
        lista = os.listdir(ruta)
        lista_db = []
    
        for i in lista: #FILTRO  LA LISTA ASI MANIPULO SOLO LOS .DB
            if i.endswith(".db"):
                lista_db.append(i)
    
        limpiar_pantalla()
        titulo = "GESTOR DE BASE DE DATOS (PRODUCTOS COMERCIALES)"
        definirMenu(titulo,"Crear Base de datos","Ingrese dato a una base",
                    "Mostrar base de datos","Ver lista bases de datos","Salir")
    
        opcion = input (">>> ")
    
        if opcion == "0":
            limpiar_pantalla()
            
            
            nombre  = input ("Ingrese nombre de la base de datos o * para volver al menu: ")
            if nombre != "*":
                crear_base(nombre)           
    
    
    
        elif opcion == "1":
            limpiar_pantalla()
            
            lista_archivos(lista_db)
            nombre  = input ("Ingrese nombre de la base de datos o * para volver al menu: ")
            if nombre != "*":
                insertar_base (nombre,lista)
            
        elif opcion == "2":
            limpiar_pantalla()
            
            lista_archivos(lista_db)
            nombre  = input ("Ingrese nombre de la base de datos o * para volver al menu: ")
            if nombre != "*":
                ver_base(nombre,lista_db)
    
        elif opcion == "3":
            limpiar_pantalla()
            if len(lista_db) == 0:
                print(f"NO HAY ARCHIVOS .DB EN LA RUTA: \n{ruta}")
            else:
                print(f"ARCHIVOS .DB EN LA RUTA: \n{ruta}\n")
                for i in lista_db:
                    print("__",i)
            input("\nPRESIONE UNA TECLA CONTINUAR ...")
            
        elif opcion == "4":
            print(">>>  Gracias por utilizar el programa  <<<")
            break
    
        else:
            #print("OPCION INCORRECTA. PRESIONE UNA TECLA CONTINUAR ...")
            #input("")
            limpiar_pantalla ()




if __name__ == "__main__":
    limpiar_pantalla ()
    
    menu()

