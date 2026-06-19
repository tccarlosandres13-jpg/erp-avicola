# ============================================
# MÓDULO: LOGIN (Logo izquierda, formulario derecha)
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
import random
from datetime import datetime

def mostrar_login():
    
    # ========== MENSAJE MOTIVACIONAL DEL DÍA ==========
    mensajes = [
        "✨ El éxito comienza con un huevo bien puesto.",
        "🐔 Cada día es una oportunidad para crecer.",
        "🥚 La calidad empieza desde el primer huevo.",
        "🌟 Doña Dora, calidad que alimenta sueños.",
        "💪 El trabajo en equipo es la clave del éxito.",
        "🌱 La constancia es la clave de la excelencia.",
        "🏆 La excelencia no es un acto, es un hábito.",
        "💛 El amor por lo que hacemos se nota en cada huevo.",
        "🚀 Cada día es una nueva oportunidad para brillar.",
        "🌈 La calidad es nuestro sello de identidad."
    ]
    
    # Seleccionar mensaje según el día del mes (cambia cada día)
    dia = datetime.now().day
    mensaje = mensajes[dia % len(mensajes)]
    
    # ========== CREAR 2 COLUMNAS: LOGO IZQUIERDA, FORMULARIO DERECHA ==========
    col_izq, col_der = st.columns([1, 1])
    
    # ========== COLUMNA IZQUIERDA: LOGO ==========
    with col_izq:
        logo = cargar_logo()
        if logo:
            # Mostrar el logo ocupando toda la columna
            st.image(logo, use_container_width=True)
        else:
            # Si no hay logo, mostrar un huevo grande
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 450px; background: white; border-radius: 20px; border: 2px solid #FFD600; padding: 20px;">
                    <span style="font-size: 180px;">🥚</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.info("💡 Sube el archivo 'logo.jpeg' o 'logo.jpg' a la raíz del repositorio para ver el logo real")
    
    # ========== COLUMNA DERECHA: FORMULARIO ==========
    with col_der:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="dora-title-geo">🥚 HUEVOS DOÑA DORA</h1>', unsafe_allow_html=True)
        st.markdown('<p class="dora-subtitle">Sistema de Gestión Avícola</p>', unsafe_allow_html=True)
        
        # Campos más pequeños (contenedor con tamaño reducido)
        with st.container():
            # Usar columnas para centrar los campos
            col_campo1, col_campo2, col_campo3 = st.columns([1, 2, 1])
            with col_campo2:
                usuario = st.text_input("👤 USUARIO", key="login_user", placeholder="Ingrese su usuario")
                password = st.text_input("🔒 CONTRASEÑA", type="password", key="login_pass", placeholder="Ingrese su contraseña")
                
                if st.button("🚪 INGRESAR", type="primary", use_container_width=True):
                    if usuario in usuarios and usuarios[usuario]["password"] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.usuario = usuario
                        st.session_state.rol = usuarios[usuario]["rol"]
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
        
        # Mensaje motivacional del día
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background: linear-gradient(135deg, #E8F5E9, #FFF9C4); border-radius: 15px; border-left: 4px solid #2E7D32;">
            <p style="font-size: 14px; color: #2E7D32; font-style: italic; margin: 0;">
                💬 {mensaje}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 Credenciales de prueba"):
            st.markdown("- **Administrador:** `admin` / `admin123`")
            st.markdown("- **Auxiliar:** `auxiliar` / `produccion123`")
        
        st.markdown('</div>', unsafe_allow_html=True)
