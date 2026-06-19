# ============================================
# MÓDULO: LOGIN (Logo izquierda - formulario + mensaje derecha)
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
from datetime import datetime
import io
import base64

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
    
    dia = datetime.now().day
    mensaje = mensajes[dia % len(mensajes)]
    
    # ========== CREAR 2 COLUMNAS ==========
    col_izq, col_der = st.columns([1, 1])
    
    # ========== COLUMNA IZQUIERDA: LOGO (ANCHO Y ALTO COMPLETO) ==========
    with col_izq:
        logo = cargar_logo()
        if logo:
            # Convertir logo a base64 para mostrarlo con altura completa
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
                    min-height: 550px;
                    max-height: 600px;
                    background: rgba(255,255,255,0.95);
                    border-radius: 20px;
                    border: 2px solid #FFD600;
                    padding: 5px;
                    overflow: hidden;
                ">
                    <img src="data:image/jpeg;base64,{img_str}" 
                         style="
                             width: 100%;
                             height: 100%;
                             object-fit: contain;
                         ">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 100vh; min-height: 550px; max-height: 600px; background: white; border-radius: 20px; border: 2px solid #FFD600; padding: 20px;">
                    <span style="font-size: 150px;">🥚</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.info("💡 Sube el archivo 'logo.jpeg' o 'logo.jpg' a la raíz del repositorio")
    
    # ========== COLUMNA DERECHA: TÍTULO + FORMULARIO + MENSAJE ==========
    with col_der:
        # TARJETA PRINCIPAL
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="dora-title-geo">🥚 HUEVOS DOÑA DORA</h1>', unsafe_allow_html=True)
        st.markdown('<p class="dora-subtitle">Sistema de Gestión Avícola</p>', unsafe_allow_html=True)
        
        # FORMULARIO
        with st.container():
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
        
        # ========== CUADRO BLANCO PEQUEÑO CON MENSAJE MOTIVACIONAL ==========
        st.markdown("""
        <div style="
            background: white;
            border-radius: 15px;
            padding: 12px 20px;
            margin: 15px auto 10px auto;
            border: 2px solid #FFD600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            text-align: center;
            max-width: 85%;
        ">
            <p style="
                font-size: 14px;
                color: #2E7D32;
                font-style: italic;
                margin: 0;
                font-weight: 500;
                line-height: 1.5;
            ">
                💬 {mensaje}
            </p>
        </div>
        """.format(mensaje=mensaje), unsafe_allow_html=True)
        
        # CREDENCIALES
        with st.expander("📋 Credenciales de prueba"):
            st.markdown("- **Administrador:** `admin` / `admin123`")
            st.markdown("- **Auxiliar:** `auxiliar` / `produccion123`")
        
        st.markdown('</div>', unsafe_allow_html=True)
