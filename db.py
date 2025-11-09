import sqlite3
import logging
from datetime import date, datetime
import os
import csv

logger = logging.getLogger(__name__)
conexion = sqlite3.connect('python_bank.db')



def crear_tablas():

    conexion.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id_dni INTEGER PRIMARY KEY,
        dni INTEGER NOT NULL UNIQUE,
        name TEXT NOT NULL,
        tipo_cliente TEXT NOT NULL);''')
    conexion.commit()
    
    conexion.execute('''CREATE TABLE IF NOT EXISTS cuentas (
        id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_dni INTEGER NOT NULL REFERENCES usuarios(dni),
        tipo_cuenta TEXT NOT NULL,
        divisa TEXT NOT NULL,
        saldo REAL DEFAULT 0.0
        );''')
    conexion.execute('''INSERT OR REPLACE INTO sqlite_sequence (name, seq)
                     VALUES ('cuentas', 1000)''')
    conexion.commit()
    
    
def registrar_user(dni, nombre, tipo_cliente):
    cursor = conexion
    cursor.execute("INSERT INTO usuarios (dni, name, tipo_cliente) VALUES (?,?,?)",
                   (dni, nombre, tipo_cliente)
                   )
    conexion.commit()
    
def crear_cuenta(id_dni, tipo_cuenta, divisa):
    try:
        with conexion:
            cursor = conexion.cursor()
            
            cursor.execute("SELECT 1 FROM usuarios WHERE id_dni = ?", (id_dni,))
            if not cursor.fetchone():
                raise ValueError(f"El usuario con DNI {id_dni} no existe")

            cursor.execute('''
                INSERT INTO cuentas (id_dni, tipo_cuenta, divisa)
                VALUES (?, ?, ?)
            ''', (id_dni, tipo_cuenta, divisa))
            
            #id_cuenta = cursor.lastrowid
            #print(f"Cuenta N°: {id_cuenta} creada como corresponde")
            return True
            
    except Exception as e:
        print(f"Error creando cuenta: {e}")
        return False
    
def buscar_usuario(campo: str, valor: str):
    CAMPOS_VALIDOS = {"dni", "name", "tipo_cliente"}
    
    if not campo or not isinstance(campo, str):
        raise ValueError("El campo debe ser una cadena no vacía")
    
    if not valor or not isinstance(valor, str):
        raise ValueError("El valor debe ser una cadena no vacía")
    
    if campo not in CAMPOS_VALIDOS:
        validos_str = ", ".join(sorted(CAMPOS_VALIDOS))
        raise ValueError(f"Campo inválido: '{campo}'. Campos válidos: {validos_str}")

    query = f"SELECT * FROM usuarios WHERE {campo} = ?"
    
    try:
        with conexion:
            cursor = conexion.cursor()
            cursor.execute(query, (valor,))
            return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error en buscar_usuario({campo}={valor}): {e}")
        raise

def id_por_dni(dni):
    cursor = conexion.cursor()
    query = f"SELECT id_dni FROM usuarios WHERE dni = ?"
    cursor.execute(query, (dni,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    return None

def buscar_cuenta_id_dni(id_dni):
    cursor = conexion.cursor()
    query = f"SELECT * FROM cuentas WHERE id_dni = ?"
    cursor.execute(query, (id_dni,))
    return cursor.fetchall()



    