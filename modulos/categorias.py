# ============================================
# MÓDULO: CATEGORÍAS DE HUEVOS
# ============================================

import streamlit as st
from modulos.datos import categorias_data, agregar_categoria, eliminar_categoria

def mostrar_categorias():
    st.title("🏷️ Gestión de Categorías de Huevos")
    st.write("### Categorías actuales")
    for cat in categorias_data["categorias"]:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"- **{cat}**")
        with col2:
            if cat not in ["Extra", "AAA", "AA", "A", "B"]:
                if st.button(f"🗑️ Eliminar {cat}", key=f"del_{cat}"):
                    if eliminar_categoria(cat):
                        st.success(f"✅ Categoría '{cat}' eliminada")
                        st.rerun()
                    else:
                        st.warning(f"⚠️ No se puede eliminar: tiene stock o es estándar")
    st.write("---")
    st.write("### Agregar nueva categoría")
    nueva_cat = st.text_input("Nombre de la nueva categoría (ej: Jumbo, C, Sucio)")
    if st.button("➕ Agregar categoría"):
        if agregar_categoria(nueva_cat.upper()):
            st.success(f"✅ Categoría '{nueva_cat.upper()}' agregada")
            st.rerun()
        else:
            st.error("❌ La categoría ya existe o está vacía")
    st.info("💡 **Nota:** Las categorías Extra, AAA, AA, A, B son estándar y no se pueden eliminar")
