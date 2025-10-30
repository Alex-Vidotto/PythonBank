import sqlite3
from datetime import date, datetime
import os
import csv

conexion = sqlite3.connect('python_bank.db')


#CREACION DE LAS TABLAS NECESARIAS PARA EL PROYECTO
def crear_tablas():
    
    conexion.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        dni INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL);''')
    
    conexion.commit()
    
def registrar_user(dni, nombre, password):
    cursor = conexion
    cursor.execute("INSERT INTO usuarios (dni, name, password) VALUES (?,?,?)",
                   (dni, nombre, password)
                   )
    conexion.commit()
    
def buscar_usuario(campo, variable):
    cursor = conexion.cursor()
    campos_validos = {"dni", "name", "password"}  
    if campo not in campos_validos:
        raise ValueError(f"Campo inválido: {campo}")
    query = f"SELECT * FROM usuarios WHERE {campo} = ?"
    cursor.execute(query, (variable,))
    usuario = cursor.fetchone()
    if usuario:
        return usuario
    return False