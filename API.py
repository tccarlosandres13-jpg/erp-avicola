# ============================================
# API PARA APP MÓVIL (Ventas)
# ============================================

import streamlit as st
import json
from datetime import datetime
from modulos.datos import cargar_datos
from modulos.ventas import cargar_ventas, cargar_clientes

def api_ventas():
    """Endpoint para consultar ventas desde app móvil"""
    ventas = cargar_ventas()
    clientes = cargar_clientes()
    
    # Preparar datos para móvil
    datos = []
    for v in ventas:
        cliente = next((c for c in clientes if c.get("id") == v.get("cliente_id")), None)
        datos.append({
            "id": v.get("id"),
            "fecha": v.get("fecha"),
            "cliente": cliente.get("nombre") if cliente else "Desconocido",
            "total_huevos": v.get("total_huevos", 0),
            "total": v.get("total", 0),
            "factura": v.get("factura", ""),
            "estado": v.get("estado", "Completada")
        })
    
    # Retornar como JSON
    return json.dumps(datos, ensure_ascii=False)

def api_clientes():
    """Endpoint para consultar clientes desde app móvil"""
    clientes = cargar_clientes()
    return json.dumps(clientes, ensure_ascii=False)
