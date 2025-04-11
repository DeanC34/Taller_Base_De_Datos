import mysql.connector
from mysql.connector import Error

import tkinter
from tkinter import *
import tkinter as _tkinter

# Cambiar todo a gestores de interfaces
# pyqt6 (Seleccionado)

#######
# Ángel Soto Pérez - S5A - 23270050 - 01/04/2025
# CRUD para el POS "Vicioso++" a interfaz
#######

# Ejemplo con tkinter

ventana = tkinter.Tk()
ventana.title ("Ventana de ejemplo")
ventana.geometry ("400x300")

etiqueta = _tkinter.Label(ventana, text="Usuarios", font=("Arial",12))
etiqueta.pack()
#place(x=170, y=10, width=100, height=20)

lbltelefono = _tkinter.Label(ventana, text="Telefono: ")
txttelefono = Entry(ventana, bg="white")
lbltelefono.place(x=10, y=30, width=100, height=20)
txttelefono.place(x=100, y=30, width=100, height=20)

lblnombre = _tkinter.Label(ventana, text="Nombre: ")
lblnombre.place(x=10, y=60, width=100, height=20)
txtnombre = Entry(ventana, bg="white")
txtnombre.place(x=100, y=60, width=100, height=20)

lbldireccion = _tkinter.Label(ventana, text="Direccion: ")
lbldireccion.place(x=10, y=90, width=100, height=20)
txtdireccion = Entry(ventana, bg="white")
txtdireccion.place(x=100, y=90, width=100, height=20)

lblrfc = _tkinter.Label(ventana, text="RFC: ")
lblrfc.place(x=10, y=120, width=100, height=20)
txtrfc = Entry(ventana, bg="white")
txtrfc.place(x=100, y=120, width=100, height=20)

lblcorreo = _tkinter.Label(ventana, text="Correo: ")
lblcorreo.place(x=10, y=150, width=100, height=20)
txtcorreo = Entry(ventana, bg="white")
txtcorreo.place(x=100, y=150, width=100, height=20)

ventana.mainloop()
