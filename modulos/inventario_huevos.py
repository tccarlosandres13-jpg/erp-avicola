# ============================================
# MÓDULO: INVENTARIO DE HUEVOS
# ============================================

import streamlit as st
import pandas as pd
from modulos.datos import inventario_huevos, categorias_data

def mostrar_inventario_huevos():
    st.title("📦 Inventario - Bodega 1 (Granja San Miguel)")
    total = inventario_huevos.get("Bodega1_total", 0)
    st.metric("Total de huevos en bodega", f"{total:,}")
    st.write("---")
    st.subheader("📊 Detalle por categoría")
    datos_inventario = []
    for cat in categorias_data["categorias"]:
        cantidad = inventario_huevos.get(f"Bodega1_{cat}", 0)
        if cantidad > 0 or total > 0:
            porcentaje = (cantidad / total * 100) if total > 0 else 0
            datos_inventario.append({"Categoría": cat, "Cantidad": f"{cantidad:,}", "Porcentaje": f"{porcentaje:.1f}%"})
    if datos_inventario:
        st.dataframe(pd.DataFrame(datos_inventario), use_container_width=True, hide_index=True)
    else:
        st.info("No hay inventario registrado aún")
