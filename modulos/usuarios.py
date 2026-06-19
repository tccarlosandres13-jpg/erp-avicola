# ============================================
# MÓDULO: USUARIOS
# ============================================

import streamlit as st
from modulos.datos import usuarios, guardar_datos, USUARIOS_FILE, hash_password

def mostrar_usuarios():
    st.title("👥 Gestión de Usuarios")
    st.write("### Usuarios actuales")
    for user, info in usuarios.items():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**{user}** - {info['nombre']} ({info['rol']})")
        with col2:
            if user != "admin":
                if st.button(f"🗑️ Eliminar {user}", key=f"del_user_{user}"):
                    del usuarios[user]
                    guardar_datos(USUARIOS_FILE, usuarios)
                    st.success(f"✅ Usuario '{user}' eliminado")
                    st.rerun()
    st.write("---")
    st.write("### Agregar nuevo usuario")
    with st.form("nuevo_usuario"):
        nuevo_user = st.text_input("Usuario")
        nuevo_nombre = st.text_input("Nombre completo")
        nuevo_pass = st.text_input("Contraseña", type="password")
        nuevo_rol = st.selectbox("Rol", ["produccion", "contador", "vendedor", "admin"])
        if st.form_submit_button("➕ Crear usuario"):
            if nuevo_user and nuevo_nombre and nuevo_pass:
                if nuevo_user not in usuarios:
                    usuarios[nuevo_user] = {"password": hash_password(nuevo_pass), "nombre": nuevo_nombre, "rol": nuevo_rol}
                    guardar_datos(USUARIOS_FILE, usuarios)
                    st.success(f"✅ Usuario '{nuevo_user}' creado")
                    st.rerun()
                else:
                    st.error("❌ El usuario ya existe")
            else:
                st.error("❌ Complete todos los campos")
