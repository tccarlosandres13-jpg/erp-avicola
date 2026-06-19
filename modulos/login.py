# ============================================
# MÓDULO: LOGIN (Diseño profesional)
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
from datetime import datetime
import io
import base64

def mostrar_login():
    
    # ========== MENSAJE MOTIVACIONAL ==========
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
    
    # ========== CREAR 2 COLUMNAS ==========
    col_izq, col_der = st.columns([1, 1])
    
    # ========== COLUMNA IZQUIERDA: LOGO ==========
    with col_izq:
        logo = cargar_logo()
        if logo:
            buffered = io.BytesIO()
            if logo.mode == 'RGBA':
                logo = logo.convert('RGB')
            logo.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: transparent;
                    padding: 0;
                ">
                    <img src="data:image/jpeg;base64,{img_str}" 
                         style="
                             width: 100%;
                             height: 100vh;
                             object-fit: contain;
                         ">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background: transparent;">
                    <span style="font-size: 180px;">🥚</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # ========== COLUMNA DERECHA: FORMULARIO PROFESIONAL ==========
    with col_der:
        st.markdown("""
        <div style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100vh;
            padding: 40px;
            max-width: 450px;
            margin: 0 auto;
        ">
            <div style="
                background: white;
                border-radius: 24px;
                padding: 45px 40px 35px 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.10);
                border: 1px solid rgba(46, 125, 50, 0.15);
                width: 100%;
            ">
                <!-- FRASE MOTIVACIONAL (arriba) -->
                <div style="
                    background: linear-gradient(135deg, #E8F5E9, #FFF9C4);
                    border-radius: 12px;
                    padding: 10px 16px;
                    margin-bottom: 25px;
                    text-align: center;
                    border-left: 4px solid #2E7D32;
                ">
                    <p style="
                        font-size: 13px;
                        color: #2E7D32;
                        font-style: italic;
                        margin: 0;
                        font-weight: 500;
                    ">
                        💬 {mensaje}
                    </p>
                </div>
                
                <!-- TÍTULO -->
                <div style="text-align: center; margin-bottom: 30px;">
                    <div style="
                        font-size: 28px;
                        font-weight: 900;
                        color: #2E7D32;
                        letter-spacing: 1px;
                        text-transform: uppercase;
                        font-family: 'Arial Black', sans-serif;
                    ">
                        🥚 HUEVOS DOÑA DORA
                    </div>
                    <div style="
                        font-size: 12px;
                        color: #F9A825;
                        font-weight: bold;
                        letter-spacing: 4px;
                        text-transform: uppercase;
                        margin-top: 4px;
                    ">
                        Sistema de Gestión Avícola
                    </div>
                </div>
        """.format(mensaje=mensaje), unsafe_allow_html=True)
        
        # FORMULARIO
        with st.container():
            usuario = st.text_input("USUARIO", key="login_user", placeholder="Ingrese su usuario")
            password = st.text_input("CONTRASEÑA", type="password", key="login_pass", placeholder="Ingrese su contraseña")
            
            if st.button("INGRESAR", type="primary", use_container_width=True):
                if usuario in usuarios and usuarios[usuario]["password"] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.session_state.rol = usuarios[usuario]["rol"]
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        
        # CREDENCIALES Y CIERRE
        with st.expander("📋 Credenciales de prueba"):
            st.markdown("- **Administrador:** `admin` / `admin123`")
            st.markdown("- **Auxiliar:** `auxiliar` / `produccion123`")
        
        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)
