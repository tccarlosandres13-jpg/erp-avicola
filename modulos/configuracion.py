# ============================================
# MÓDULO: CONFIGURACIÓN
# ============================================

import streamlit as st
from modulos.datos import galpones, guardar_datos, GALPONES_FILE, inventario_gallinas

def mostrar_configuracion():
    st.title("⚙️ Configuración de Galpones")
    st.write("### Galpones registrados")
    for i, galpon in enumerate(galpones):
        with st.expander(f"📌 {galpon['nombre']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                nuevo_nombre = st.text_input("Nombre", value=galpon['nombre'], key=f"nombre_{i}")
            with col2:
                nueva_cantidad = st.number_input("Cantidad de gallinas", value=galpon['cantidad_gallinas'], key=f"cantidad_{i}")
            with col3:
                nuevo_estado = st.selectbox("Estado", ["produccion", "mantenimiento", "descanso", "descarte"], index=["produccion", "mantenimiento", "descanso", "descarte"].index(galpon['estado']), key=f"estado_{i}")
            if st.button(f"💾 Guardar cambios", key=f"guardar_{i}"):
                galpones[i]["nombre"] = nuevo_nombre
                galpones[i]["cantidad_gallinas"] = nueva_cantidad
                galpones[i]["estado"] = nuevo_estado
                guardar_datos(GALPONES_FILE, galpones)
                st.success(f"✅ Galpón actualizado")
                st.rerun()
    st.write("---")
    st.write("### Agregar nuevo galpón")
    with st.form("nuevo_galpon"):
        nombre_galpon = st.text_input("Nombre del galpón")
        gallinas_galpon = st.number_input("Cantidad de gallinas", min_value=0, value=0)
        estado_galpon = st.selectbox("Estado", ["produccion", "mantenimiento", "descanso", "descarte"])
        if st.form_submit_button("➕ Agregar galpón"):
            if nombre_galpon:
                nuevo_id = max([g["id"] for g in galpones]) + 1 if galpones else 1
                galpones.append({"id": nuevo_id, "nombre": nombre_galpon, "cantidad_gallinas": gallinas_galpon, "estado": estado_galpon})
                guardar_datos(GALPONES_FILE, galpones)
                inventario_gallinas[str(nuevo_id)] = {"nombre": nombre_galpon, "cantidad": gallinas_galpon, "estado": estado_galpon}
                guardar_datos(GALPONES_FILE, inventario_gallinas)
                st.success(f"✅ Galpón '{nombre_galpon}' agregado")
                st.rerun()
            else:
                st.error("❌ El nombre es obligatorio")
