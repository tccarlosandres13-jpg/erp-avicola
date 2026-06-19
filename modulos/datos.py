# ============================================
# DATOS Y FUNCIONES COMPARTIDAS
# ============================================

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import json
import os
from PIL import Image

# ============================================
# ARCHIVOS DE DATOS
# ============================================

USUARIOS_FILE = 'usuarios.json'
GALPONES_FILE = 'galpones.json'
PRODUCCION_FILE = 'produccion.json'
INVENTARIO_HUEVOS_FILE = 'inventario.json'
CATEGORIAS_FILE = 'categorias.json'
INVENTARIO_GALLINAS_FILE = 'inventario_gallinas.json'
MOVIMIENTOS_GALLINAS_FILE = 'movimientos_gallinas.json'

# ============================================
# FUNCIONES DE CARGA/GUARDADO
# ============================================

def cargar_datos(archivo, por_defecto):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return por_defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============================================
# DATOS POR DEFECTO
# ============================================

USUARIOS_POR_DEFECTO = {
    "admin": {"password": hash_password("admin123"), "nombre": "Administrador", "rol": "admin"},
    "auxiliar": {"password": hash_password("produccion123"), "nombre": "Auxiliar de Producción", "rol": "produccion"}
}

GALPONES_POR_DEFECTO = [
    {"id": 1, "nombre": "Galpón 1", "cantidad_gallinas": 75000, "estado": "produccion"},
    {"id": 2, "nombre": "Galpón 2", "cantidad_gallinas": 0, "estado": "mantenimiento"},
    {"id": 3, "nombre": "Galpón 3", "cantidad_gallinas": 25000, "estado": "produccion"},
    {"id": 4, "nombre": "Galpón Levante", "cantidad_gallinas": 0, "estado": "descanso"}
]

CATEGORIAS_POR_DEFECTO = {"categorias": ["Extra", "AAA", "AA", "A", "B"], "editable": True}

# ============================================
# CARGA INICIAL DE DATOS
# ============================================

usuarios = cargar_datos(USUARIOS_FILE, USUARIOS_POR_DEFECTO)
galpones = cargar_datos(GALPONES_FILE, GALPONES_POR_DEFECTO)
produccion = cargar_datos(PRODUCCION_FILE, [])
inventario_huevos = cargar_datos(INVENTARIO_HUEVOS_FILE, {})
categorias_data = cargar_datos(CATEGORIAS_FILE, CATEGORIAS_POR_DEFECTO)
inventario_gallinas = cargar_datos(INVENTARIO_GALLINAS_FILE, {})
movimientos_gallinas = cargar_datos(MOVIMIENTOS_GALLINAS_FILE, [])

if not inventario_gallinas:
    for g in galpones:
        inventario_gallinas[str(g["id"])] = {"nombre": g["nombre"], "cantidad": g["cantidad_gallinas"], "estado": g["estado"]}
    guardar_datos(INVENTARIO_GALLINAS_FILE, inventario_gallinas)

if not inventario_huevos:
    for cat in categorias_data["categorias"]:
        inventario_huevos[f"Bodega1_{cat}"] = 0
    inventario_huevos["Bodega1_total"] = 0
    guardar_datos(INVENTARIO_HUEVOS_FILE, inventario_huevos)

# ============================================
# FUNCIONES DE NEGOCIO
# ============================================

def registrar_movimiento_gallinas(galpon_id, tipo_movimiento, cantidad, motivo, fecha):
    galpon = next((g for g in galpones if g["id"] == galpon_id), None)
    if not galpon:
        return False, "Galpón no encontrado"
    cantidad_actual = inventario_gallinas.get(str(galpon_id), {}).get("cantidad", 0)
    if tipo_movimiento == "mortalidad":
        nueva_cantidad = cantidad_actual - cantidad
        if nueva_cantidad < 0:
            return False, "No se puede registrar mortalidad mayor a las gallinas existentes"
    elif tipo_movimiento == "levante":
        nueva_cantidad = cantidad_actual + cantidad
    elif tipo_movimiento == "descarte":
        nueva_cantidad = cantidad_actual - cantidad
        if nueva_cantidad < 0:
            return False, "No se puede registrar descarte mayor a las gallinas existentes"
    else:
        return False, "Tipo de movimiento no válido"
    movimiento = {"id": len(movimientos_gallinas) + 1, "galpon_id": galpon_id, "galpon_nombre": galpon["nombre"], "fecha": fecha, "tipo": tipo_movimiento, "cantidad": cantidad, "motivo": motivo, "cantidad_anterior": cantidad_actual, "cantidad_nueva": nueva_cantidad}
    movimientos_gallinas.append(movimiento)
    guardar_datos(MOVIMIENTOS_GALLINAS_FILE, movimientos_gallinas)
    inventario_gallinas[str(galpon_id)] = {"nombre": galpon["nombre"], "cantidad": nueva_cantidad, "estado": galpon["estado"]}
    guardar_datos(INVENTARIO_GALLINAS_FILE, inventario_gallinas)
    for g in galpones:
        if g["id"] == galpon_id:
            g["cantidad_gallinas"] = nueva_cantidad
            break
    guardar_datos(GALPONES_FILE, galpones)
    return True, movimiento

def obtener_postura_real_periodo(galpon_id, fecha_inicio, fecha_fin):
    producciones_galpon = [p for p in produccion if p["galpon_id"] == galpon_id and fecha_inicio <= p["fecha"] <= fecha_fin]
    if not producciones_galpon:
        return 0
    total_huevos = sum(p["total_huevos"] for p in producciones_galpon)
    promedio_diario = total_huevos / len(producciones_galpon)
    cantidad_gallinas = inventario_gallinas.get(str(galpon_id), {}).get("cantidad", 0)
    if cantidad_gallinas == 0:
        return 0
    return round((promedio_diario / cantidad_gallinas) * 100, 1)

def obtener_mortalidad_periodo(galpon_id, fecha_inicio, fecha_fin):
    return sum(m["cantidad"] for m in movimientos_gallinas if m["galpon_id"] == galpon_id and m["tipo"] == "mortalidad" and fecha_inicio <= m["fecha"] <= fecha_fin)

def registrar_produccion(galpon_id, fecha, clasificacion):
    nuevo_registro = {"id": len(produccion) + 1, "galpon_id": galpon_id, "fecha": fecha, "clasificacion": clasificacion, "total_huevos": sum(clasificacion.values())}
    produccion.append(nuevo_registro)
    guardar_datos(PRODUCCION_FILE, produccion)
    for categoria, cantidad in clasificacion.items():
        inventario_huevos[f"Bodega1_{categoria}"] = inventario_huevos.get(f"Bodega1_{categoria}", 0) + cantidad
        inventario_huevos["Bodega1_total"] = inventario_huevos.get("Bodega1_total", 0) + cantidad
    guardar_datos(INVENTARIO_HUEVOS_FILE, inventario_huevos)
    return nuevo_registro

def agregar_categoria(nueva_categoria):
    if nueva_categoria and nueva_categoria not in categorias_data["categorias"]:
        categorias_data["categorias"].append(nueva_categoria)
        guardar_datos(CATEGORIAS_FILE, categorias_data)
        inventario_huevos[f"Bodega1_{nueva_categoria}"] = 0
        guardar_datos(INVENTARIO_HUEVOS_FILE, inventario_huevos)
        return True
    return False

def eliminar_categoria(categoria):
    if categoria in categorias_data["categorias"] and categoria not in ["Extra", "AAA", "AA", "A", "B"]:
        if inventario_huevos.get(f"Bodega1_{categoria}", 0) == 0:
            categorias_data["categorias"].remove(categoria)
            guardar_datos(CATEGORIAS_FILE, categorias_data)
            return True
    return False

def cargar_logo():
    logo_path = "logo.jpeg"
    if os.path.exists(logo_path):
        return Image.open(logo_path)
    else:
        logo_path_jpg = "logo.jpg"
        if os.path.exists(logo_path_jpg):
            return Image.open(logo_path_jpg)
    return None
