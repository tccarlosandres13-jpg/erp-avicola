# ============================================
# MÓDULO: LOGIN (Corregido)
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
            st.markdown('<div style="text-align:center;font-size:150px;padding:50px;">🥚</div>', unsafe_allow_html=True)
    
    with col_der:
        st.markdown("""
            <div style="text-align:center;margin-bottom:5px;">
                <div style="font-size:28px;font-weight:900;color:#FFD600;letter-spacing:1px;text-transform:uppercase;">
                    🥚 HUEVOS DOÑA DORA
                </div>
                <div style="font-size:12px;color:rgba(255,255,255,0.5);font-weight:bold;letter-spacing:3px;text-transform:uppercase;margin-top:2px;">
                    Sistema de Gestión Avícola
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="
                background: rgba(255,214,0,0.08);
                border-radius: 10px;
                padding: 10px 15px;
                margin: 15px 0 25px 0;
                text-align: center;
                border-left: 4px solid #FFD600;
            ">
                <p style="font-size:14px;color:#FFD600;font-style:italic;margin:0;font-weight:500;">
                    💬 {mensaje}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        usuario = st.text_input("", placeholder="👤 Ingrese su usuario", key="login_user")
        password = st.text_input("", placeholder="🔒 Ingrese su contraseña", type="password", key="login_pass")
        
        if st.button("🚪 INGRESAR", type="primary", use_container_width=True):
            if usuario in usuarios and usuarios[usuario]["password"] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.usuario = usuario
                st.session_state.rol = usuarios[usuario]["rol"]
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
        
        with st.expander("📋 Credenciales de prueba"):
            st.markdown("- **Administrador:** `admin` / `admin123`")
            st.markdown("- **Auxiliar:** `auxiliar` / `produccion123`")
