# ============================================
# MÓDULO: LOGIN - Diseño profesional limpio
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
from datetime import datetime

def mostrar_login():
    
    # Mensaje motivacional que cambia cada día
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
    
    # ========== DOS COLUMNAS ==========
    col_izq, col_der = st.columns([1, 1])
    
    # ========== COLUMNA IZQUIERDA ==========
    with col_izq:
        logo = cargar_logo()
        if logo:
            st.image(logo, use_container_width=True)
        else:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
                    <span style="font-size: 200px;">🥚</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # ========== COLUMNA DERECHA ==========
    with col_der:
        
        # TARJETA BLANCA
        st.markdown(
            """
            <div style="
                background: white;
                border-radius: 20px;
                padding: 40px 35px 35px 35px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.08);
                border: 1px solid #e8f5e9;
                max-width: 420px;
                margin: 0 auto;
            ">
                <!-- TÍTULO -->
                <div style="text-align: center; margin-bottom: 8px;">
                    <div style="
                        font-size: 24px;
                        font-weight: 900;
                        color: #2E7D32;
                        letter-spacing: 1px;
                        text-transform: uppercase;
                        font-family: 'Arial Black', sans-serif;
                    ">
                        🥚 HUEVOS DOÑA DORA
                    </div>
                    <div style="
                        font-size: 11px;
                        color: #F9A825;
                        font-weight: bold;
                        letter-spacing: 3px;
                        text-transform: uppercase;
                        margin-top: 2px;
                    ">
                        Sistema de Gestión Avícola
                    </div>
                </div>
                
                <!-- FRASE MOTIVACIONAL -->
                <div style="
                    background: #f0f7f0;
                    border-radius: 10px;
                    padding: 10px 15px;
                    margin: 18px 0 25px 0;
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
                        💬 """ + mensaje + """
                    </p>
                </div>
            """,
            unsafe_allow_html=True
        )
        
        # FORMULARIO
        usuario = st.text_input(
            "USUARIO",
            key="login_user",
            placeholder="Ingrese su usuario",
            label_visibility="collapsed"
        )
        
        password = st.text_input(
            "CONTRASEÑA",
            type="password",
            key="login_pass",
            placeholder="Ingrese su contraseña",
            label_visibility="collapsed"
        )
        
        # BOTÓN
        if st.button("INGRESAR", type="primary", use_container_width=True):
            if usuario in usuarios and usuarios[usuario]["password"] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.usuario = usuario
                st.session_state.rol = usuarios[usuario]["rol"]
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
        
        # CREDENCIALES
        with st.expander("📋 Credenciales de prueba"):
            st.markdown("""
            - **Administrador:** `admin` / `admin123`
            - **Auxiliar:** `auxiliar` / `produccion123`
            """)
        
        # CERRAR TARJETA
        st.markdown("</div>", unsafe_allow_html=True)
