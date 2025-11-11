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
        id_dni INTEGER NOT NULL,
        tipo_cuenta TEXT NOT NULL,
        divisa TEXT NOT NULL,
        saldo REAL DEFAULT 0.0,
        tiempo INTEGER DEFAULT 0,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_dni) REFERENCES usuarios(id_dni)
    );''')
    conexion.execute('''INSERT OR REPLACE INTO sqlite_sequence (name, seq)
                     VALUES ('cuentas', 1000)''')
    conexion.commit()
    
    conexion.execute('''CREATE TABLE IF NOT EXISTS operaciones (
        id_operaciones INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_operacion TEXT NOT NULL,
        id_cuenta_origen INTEGER NOT NULL REFERENCES cuentas(id_cuenta),
        id_cuenta_destino INTEGER REFERENCES cuentas(id_cuenta),
        monto REAL NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')
    conexion.commit()
    
    conexion.execute('''CREATE TABLE IF NOT EXISTS comisiones (
        id_comision INTEGER PRIMARY KEY AUTOINCREMENT,
        id_operacion INTEGER NOT NULL REFERENCES operaciones(id_operaciones),
        monto_comision REAL NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')
    conexion.commit()
    
    conexion.execute('''CREATE TABLE IF NOT EXISTS mentenimientos (
        id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cuenta INTEGER NOT NULL REFERENCES cuentas(id_cuenta),
        monto_mantenimiento REAL NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')
    conexion.commit()
    
    
def registrar_user(dni, nombre, tipo_cliente):
    try:
        with conexion:
            cursor = conexion
            cursor.execute("INSERT INTO usuarios (dni, name, tipo_cliente) VALUES (?,?,?)",
                           (dni, nombre, tipo_cliente)
                           )
            return True
    except Exception as e:
        print(f"Error registrando usuario: {e}")
        return False
    
def crear_cuenta(dni, tipo_cuenta, divisa):
    try:
        with conexion:
            cursor = conexion.cursor()
            
            cursor.execute("SELECT 1 FROM usuarios WHERE id_dni = ?", (dni,))
            if not cursor.fetchone():
                raise ValueError(f"El usuario con DNI {dni} no existe")

            cursor.execute('''
                INSERT INTO cuentas (id_dni, tipo_cuenta, divisa)
                VALUES (?, ?, ?)
            ''', (dni, tipo_cuenta, divisa))
            
            return True
            
    except Exception as e:
        print(f"Error creando cuenta: {e}")
        return False
    
def crear_cuenta_plazo_fijo(dni, tipo_cuenta, divisa, tiempo, monto):
    try:
        with conexion:
            cursor = conexion.cursor()
            
            # Verificar si el usuario existe
            cursor.execute("SELECT 1 FROM usuarios WHERE id_dni = ?", (dni,))
            if not cursor.fetchone():
                raise ValueError(f"El usuario con ID {dni} no existe")

            # Insertar cuenta de plazo fijo con monto inicial
            cursor.execute('''
                INSERT INTO cuentas (id_dni, tipo_cuenta, divisa, saldo, tiempo)
                VALUES (?, ?, ?, ?, ?)
            ''', (dni, tipo_cuenta, divisa, monto, tiempo))
            
            # Registrar la operación
            id_cuenta = cursor.lastrowid
            cursor.execute('''
                INSERT INTO operaciones (tipo_operacion, id_cuenta_origen, monto)
                VALUES (?, ?, ?)
            ''', ('CREACION_PLAZO_FIJO', id_cuenta, monto))
            
            print(f"Plazo fijo creado: Cuenta N° {id_cuenta}, Monto: {monto}, Días: {tiempo}")
            return True
            
    except Exception as e:
        print(f"Error creando plazo fijo: {e}")
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

def buscar_cuenta_por_id(id_cuenta):
    cursor = conexion.cursor()
    query = f"SELECT * FROM cuentas WHERE id_cuenta = ?"
    cursor.execute(query, (id_cuenta,))
    return cursor.fetchone()

def buscar_cuenta_id_dni(id_dni):
    cursor = conexion.cursor()
    query = f"SELECT * FROM cuentas WHERE id_dni = ?"
    cursor.execute(query, (id_dni,))
    return cursor.fetchall()

def saldo_actual_cuenta(id_cuenta):
    cursor = conexion.cursor()
    query = f"SELECT saldo FROM cuentas WHERE id_cuenta = ?"
    cursor.execute(query, (id_cuenta,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    return 0.0
    
def registrar_operaciones(tipo_operacion, id_cuenta_origen, id_cuenta_destino, monto):
    try:
        with conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO operaciones (tipo_operacion, id_cuenta_origen, id_cuenta_destino, monto) VALUES (?,?,?,?)"
            cursor.execute(query, (tipo_operacion, id_cuenta_origen, id_cuenta_destino, monto))
            return True
    except Exception as e:
        logger.error(f"Error registrando operacion: {e}")
        return False


# OPERACIONES DE BANCO

def depositar_dinero(id_cuenta, monto):
    try:
        with conexion:
            cursor = conexion.cursor()
            query = "UPDATE cuentas SET saldo = saldo + ? WHERE id_cuenta = ?"
            cursor.execute(query, (monto, id_cuenta))
            return True
    except Exception as e:
        logger.error(f"Error depositando dinero: {e}")
        return False
    
def retirar_dinero(id_cuenta, monto):
    try:
        with conexion:
            cursor = conexion.cursor()
            query = "UPDATE cuentas SET saldo = saldo - ? WHERE id_cuenta = ?"
            cursor.execute(query, (monto, id_cuenta))
            return True
    except Exception as e:
        logger.error(f"Error retirando dinero: {e}")
        return False
            
    