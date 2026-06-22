# ============================================
# MÓDULO: LOGIN (Diseño Premium)
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
    
    # Fondo con efecto gradiente premium
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a1a0a 0%, #1a3a1a 40%, #2d5a2d 100%) !important;
        }
        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.08) !important;
            border: 2px solid rgba(255,255,255,0.15) !important;
            border-radius: 16px !important;
            color: white !important;
            font-size: 16px !important;
            padding: 14px 20px !important;
            height: 55px !important;
            backdrop-filter: blur(10px) !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #FFD600 !important;
            box-shadow: 0 0 30px rgba(255,214,0,0.15) !important;
            background: rgba(255,255,255,0.12) !important;
        }
        .stTextInput > div > div > input::placeholder {
            color: rgba(255,255,255,0.5) !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #FFD600, #F9A825) !important;
            color: #1a3a1a !important;
            border-radius: 16px !important;
            padding: 14px !important;
            font-weight: 800 !important;
            font-size: 18px !important;
            border: none !important;
            box-shadow: 0 8px 30px rgba(255,214,0,0.3) !important;
            transition: all 0.3s ease !important;
            height: 55px !important;
            letter-spacing: 2px !important;
        }
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 12px 50px rgba(255,214,0,0.5) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        logo = cargar_logo()
        if logo:
            st.image(logo, use_container_width=True)
        else:
            st.markdown("""
            <div style="display:flex;justify-content:center;align-items:center;height:80vh;">
                <span style="font-size:200px;filter:drop-shadow(0 20px 60px rgba(255,214,0,0.3));">🥚</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_der:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 50px 40px 40px 40px;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 30px 80px rgba(0,0,0,0.4);
            max-width: 440px;
            margin: 0 auto;
        ">
            <div style="text-align:center;margin-bottom:10px;">
                <div style="font-size:32px;font-weight:900;color:#FFD600;letter-spacing:3px;text-transform:uppercase;text-shadow:0 0 40px rgba(255,214,0,0.2);">
                    🥚 HUEVOS DOÑA DORA
                </div>
                <div style="font-size:13px;color:rgba(255,255,255,0.6);font-weight:600;letter-spacing:6px;text-transform:uppercase;margin-top:4px;">
                    Sistema de Gestión Avícola
                </div>
            </div>
            
            <div style="
                background: rgba(255,214,0,0.08);
                border-radius: 14px;
                padding: 14px 20px;
                margin: 22px 0 28px 0;
                text-align: center;
                border-left: 4px solid #FFD600;
                border-right: 4px solid #FFD600;
            ">
                <p style="font-size:15px;color:#FFD600;font-style:italic;margin:0;font-weight:500;">
                    💬 """ + mensaje + """
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        usuario = st.text_input("", placeholder="👤 Ingrese su usuario", key="login_user")
        password = st.text_input("", placeholder="🔒 Ingrese su contraseña", type="password", key="login_pass")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 INGRESAR", type="primary", use_container_width=True):
                if usuario in usuarios and usuarios[usuario]["password"] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.session_state.rol = usuarios[usuario]["rol"]
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        
        st.markdown("""
        <div style="text-align:center;margin-top:12px;">
            <span style="color:rgba(255,255,255,0.3);font-size:13px;letter-spacing:2px;">Credenciales: admin / admin123</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
