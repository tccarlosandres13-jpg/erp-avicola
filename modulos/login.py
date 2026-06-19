# ============================================
# MÓDULO: LOGIN (Versión simplificada y funcional)
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
from datetime import datetime
import io
import base64

def mostrar_login():
    
    # ========== MENSAJE MOTIVACIONAL ==========
    mensaje = "💬 La calidad es nuestro sello de identidad."
    
    # ========== CREAR 2 COLUMNAS ==========
    col_izq, col_der = st.columns([1, 1])
    
    # ========== COLUMNA IZQUIERDA: LOGO ==========
    with col_izq:
        logo = cargar_logo()
        if logo:
            # Redimensionar logo para que se vea bien
            st.image(logo, use_container_width=True)
        else:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
                    <span style="font-size: 180px;">🥚</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # ========== COLUMNA DERECHA: FORMULARIO ==========
    with col_der:
        # Título
        st.markdown("""
            <div style="text-align: center; margin-bottom: 10px;">
                <div style="font-size: 28px; font-weight: 900; color: #2E7D32; letter-spacing: 2px; text-transform: uppercase; font-family: 'Arial Black', sans-serif;">
                    🥚 HUEVOS DOÑA DORA
                </div>
                <div style="font-size: 12px; color: #F9A825; font-weight: bold; letter-spacing: 4px; text-transform: uppercase; margin-top: 2px;">
                    Sistema de Gestión Avícola
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Frase motivacional
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #E8F5E9, #FFF9C4);
                border-radius: 12px;
                padding: 12px 16px;
                margin-bottom: 25px;
                text-align: center;
                border-left: 4px solid #2E7D32;
            ">
                <p style="font-size: 14px; color: #2E7D32; font-style: italic; margin: 0; font-weight: 500;">
                    {mensaje}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # ========== FORMULARIO (con labels visibles) ==========
        with st.container():
            usuario = st.text_input("👤 USUARIO", key="login_user", placeholder="Ingrese su usuario")
            password = st.text_input("🔒 CONTRASEÑA", type="password", key="login_pass", placeholder="Ingrese su contraseña")
            
            # Botón centrado
            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b2:
                if st.button("🚪 INGRESAR", type="primary", use_container_width=True):
                    if usuario in usuarios and usuarios[usuario]["password"] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.usuario = usuario
                        st.session_state.rol = usuarios[usuario]["rol"]
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
        
        # Credenciales
        with st.expander("📋 Credenciales de prueba"):
            st.markdown("- **Administrador:** `admin` / `admin123`")
            st.markdown("- **Auxiliar:** `auxiliar` / `produccion123`")
