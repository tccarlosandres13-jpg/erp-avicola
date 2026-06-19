# ============================================
# MÓDULO: DASHBOARD
# ============================================

import streamlit as st
from datetime import datetime
from modulos.datos import produccion, inventario_huevos, inventario_gallinas, movimientos_gallinas, galpones

def mostrar_dashboard():
    st.title("🏠 Dashboard - Resumen del Día")
    col1, col2, col3, col4 = st.columns(4)
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    total_inventario = inventario_huevos.get("Bodega1_total", 0)
    total_gallinas = sum(g.get("cantidad", 0) for g in inventario_gallinas.values())
    mes_actual = datetime.now().strftime("%Y-%m")
    mortalidad_mes = sum(m["cantidad"] for m in movimientos_gallinas if m["tipo"] == "mortalidad" and m["fecha"].startswith(mes_actual))
    col1.metric("🥚 Producción Hoy", f"{total_hoy:,} huevos")
    col2.metric("📦 Inventario Bodega 1", f"{total_inventario:,} huevos")
    col3.metric("🐔 Gallinas Vivas", f"{total_gallinas:,}")
    col4.metric("⚠️ Mortalidad (mes)", f"{mortalidad_mes:,}")
    st.write("---")
    st.subheader("📈 Últimas Producciones")
    if produccion:
        ultimas = produccion[-5:][::-1]
        for p in ultimas:
            galpon_nombre = next((g["nombre"] for g in galpones if g["id"] == p["galpon_id"]), "Desconocido")
            st.write(f"**{p['fecha']} - {galpon_nombre}**: {p['total_huevos']:,} huevos")
    else:
        st.info("No hay registros de producción aún.")
