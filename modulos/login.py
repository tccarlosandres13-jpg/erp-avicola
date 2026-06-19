# ============================================
# MÓDULO: LOGIN (Diseño moderno y vibrante)
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
from datetime import datetime

def mostrar_login():
    
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
    
    dia = datetime.now().day
    mensaje = mensajes[dia % len(mensajes)]
    
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        logo = cargar_logo()
        if logo:
            st.image(logo, use_container_width=True)
        else:
            st.markdown("""
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                height: 80vh;
            ">
                <span style="font-size: 200px; filter: drop-shadow(0 10px 30px rgba(0,0,0,0.1));">🥚</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_der:
        st.markdown("""
        <div style="
            background: white;
            border-radius: 24px;
            padding: 45px 40px 35px 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.12);
            border: 1px solid rgba(46, 125, 50, 0.08);
            max-width: 420px;
            margin: 0 auto;
        ">
            <div style="text-align: center; margin-bottom: 8px;">
                <div style="
                    font-size: 30px;
                    font-weight: 900;
                    color: #2E7D32;
                    letter-spacing: 2px;
                    text-transform: uppercase;
                    font-family: 'Arial Black', sans-serif;
                    text-shadow: 0 2px 10px rgba(46,125,50,0.1);
                ">
                    🥚 HUEVOS DOÑA DORA
                </div>
                <div style="
                    font-size: 13px;
                    color: #F9A825;
                    font-weight: 700;
                    letter-spacing: 5px;
                    text-transform: uppercase;
                    margin-top: 4px;
                ">
                    Sistema de Gestión Avícola
                </div>
            </div>
            
            <div style="
                background: linear-gradient(135deg, #e8f5e9, #fff9c4);
                border-radius: 12px;
                padding: 12px 18px;
                margin: 20px 0 25px 0;
                text-align: center;
                border-left: 4px solid #2E7D32;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            ">
                <p style="
                    font-size: 14px;
                    color: #2E7D32;
                    font-style: italic;
                    margin: 0;
                    font-weight: 500;
                ">
                    💬 """ + mensaje + """
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Campos con estilo moderno
        usuario = st.text_input("", placeholder="👤 Ingrese su usuario", key="login_user")
        password = st.text_input("", placeholder="🔒 Ingrese su contraseña", type="password", key="login_pass")
        
        # Botón con efecto brillante
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚪 INGRESAR", type="primary", use_container_width=True):
                if usuario in usuarios and usuarios[usuario]["password"] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.session_state.rol = usuarios[usuario]["rol"]
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        
        with st.expander("📋 Credenciales de prueba"):
            st.markdown("""
            <div style="font-size: 14px;">
                - **Administrador:** `admin` / `admin123`<br>
                - **Auxiliar:** `auxiliar` / `produccion123`
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
