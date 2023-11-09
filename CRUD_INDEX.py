from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

#DEFINICION DE VARIABLES
MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIMEOUT=1000
MONGO_URL="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"
DB_MONGO="Nomina"
TABLA_MONGO="Empleados"
cliente=pymongo.MongoClient(MONGO_URL,ServerSelectionTimeoutMS=MONGO_TIMEOUT)
DB=cliente[DB_MONGO]
TABLA=DB[TABLA_MONGO]
KEY=""

#CONSULTAR TODOS LOS REGISTROS DE LA BD
def imprimir():
    try:
        historial=principal.get_children()
        for celda in historial:
            principal.delete(celda)
        for registros in TABLA.find():
            principal.insert('',0,text=registros["_id"],values=registros["Nombre"])
    except pymongo.errors.ServerSelectionTimeoutError as ErrorTiempo:
        print("Tiempo excedido"+ErrorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al intentar conectarse")

#CREAR NUEVOS REGISTROS EN LA BD
def crear():
    if len(nombre.get())!=0 and len(salario.get())!=0 :
        try:
            registros={"Nombre":nombre.get(),"Salario":salario.get()}
            TABLA.insert_one(registros)
            nombre.delete(0,END)
            salario.delete(0,END)
            imprimir()
        except pymongo.errors.ConnectionFailure as error: 
            print(error)
    else:
        messagebox.showerror(message="DEBE LLENAR INFORMACION")
        imprimir()

#Seleccionar uno de los registros mostrados en la tabla presionando doble click
def click(event):
    global KEY
    KEY=str(principal.item(principal.selection())["text"])
    fila=TABLA.find({"_id":ObjectId(KEY)})[0]
    nombre.delete(0,END)
    nombre.insert(0,fila["Nombre"])
    salario.delete(0,END)
    salario.insert(0,fila["Salario"])

#Editar registros seleccionados
def editar():
    global KEY
    if len(nombre.get())!=0 and len(salario.get())!=0:
        try:
            Search={"_id":ObjectId(KEY)}
            update={"Nombre":nombre.get(),"Salario":salario.get()}
            TABLA.update(Search,update)
            nombre.delete(0,END)
            salario.delete(0,END)
            imprimir()
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="DEBE LLENAR INFORMACION")
        imprimir()    
    insertar["state"]="normal"
    editar["state"]="disabled"
    suprimir["state"]="disabled"

#Eliminar registros seleccionados
def suprimir():
    global KEY
    try:
        Search={"_id":ObjectId(KEY)}
        TABLA.delete_one(Search)
        nombre.delete(0,END)
        salario.delete(0,END)
        imprimir()
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    
    insertar["state"]="disabled"
    editar["state"]="disabled"
    suprimir["state"]="normal"


#Definición modelo gráfico.
ventana=Tk()
principal=ttk.Treeview(ventana,columns=2)
principal.grid(row=1,column=0,columnspan=2)
principal.heading("#0",text="ID")
principal.heading("#1",text="NOMBRE")
principal.bind("<Double-Button-1>",click)

Label(ventana,text="NOMBRE").grid(row=2,column=0)
nombre=Entry(ventana)
nombre.grid(row=2,column=1)

Label(ventana,text="SALARIO").grid(row=3,column=0)
salario=Entry(ventana)
salario.grid(row=3,column=1)

insertar=Button(ventana,text="Insertar registro",command=crear,bg="purple",fg="white")
insertar.grid(row=4,columnspan=2,sticky=W+E)

editar=Button(ventana,text="Editar registro",command=editar,bg="purple",fg="white")
editar.grid(row=6,columnspan=2,sticky=W+E)

suprimir=Button(ventana,text="Eliminar registro",command=suprimir,bg="purple",fg="white")
suprimir.grid(row=8,columnspan=2,sticky=W+E)


imprimir()
principal.mainloop()