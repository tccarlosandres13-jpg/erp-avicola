# ============================================
# MÓDULO: LOGIN (Logo izquierda, formulario derecha)
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
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
    
    dia = datetime.now().day
    mensaje = mensajes[dia % len(mensajes)]
    
    # ========== CREAR 2 COLUMNAS ==========
    col_izq, col_der = st.columns([1, 1])
    
    # ========== COLUMNA IZQUIERDA: LOGO (ANCHO Y ALTO COMPLETO) ==========
    with col_izq:
        logo = cargar_logo()
        if logo:
            # Usar contenedor con altura completa
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100%;
                    min-height: 520px;
                    background: rgba(255,255,255,0.9);
                    border-radius: 20px;
                    border: 2px solid #FFD600;
                    padding: 10px;
                    overflow: hidden;
                ">
                    <img src="data:image/jpeg;base64,{logo_para_html(logo)}" 
                         style="
                             width: 100%;
                             height: 100%;
                             max-height: 500px;
                             object-fit: contain;
                         ">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 520px; background: white; border-radius: 20px; border: 2px solid #FFD600; padding: 20px;">
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
        
        # ========== MENSAJE MOTIVACIONAL DENTRO DE CUADRO BLANCO PEQUEÑO ==========
        st.markdown("---")
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 8px 15px;
            margin: 5px 0 15px 0;
            border-left: 4px solid #2E7D32;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            text-align: center;
            max-width: 80%;
            margin-left: auto;
            margin-right: auto;
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
        """, unsafe_allow_html=True)
        
        with st.expander("📋 Credenciales de prueba"):
            st.markdown("- **Administrador:** `admin` / `admin123`")
            st.markdown("- **Auxiliar:** `auxiliar` / `produccion123`")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FUNCIÓN PARA CONVERTIR LOGO A BASE64
# ============================================

def logo_para_html(logo):
    import io
    import base64
    from PIL import Image
    
    # Convertir la imagen a bytes
    buffered = io.BytesIO()
    if logo.mode == 'RGBA':
        logo = logo.convert('RGB')
    logo.save(buffered, format="JPEG", quality=85)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str
