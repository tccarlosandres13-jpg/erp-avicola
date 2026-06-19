# ============================================
# MÓDULO: LOGIN (Diseño en 2 columnas)
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo

def mostrar_login():
    
    # Crear 2 columnas: izquierda (formulario) y derecha (logo)
    col_izq, col_der = st.columns([1, 1])
    
    # ========== COLUMNA IZQUIERDA: FORMULARIO ==========
    with col_izq:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="dora-title">🥚 HUEVOS DOÑA DORA</h1>', unsafe_allow_html=True)
        st.markdown('<p class="dora-subtitle">Sistema de Gestión Avícola</p>', unsafe_allow_html=True)
        
        usuario = st.text_input("👤 USUARIO", key="login_user", placeholder="Ingrese su usuario")
        password = st.text_input("🔒 CONTRASEÑA", type="password", key="login_pass", placeholder="Ingrese su contraseña")
        
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
            st.markdown("- **Administrador:** `admin` / `admin123`")
            st.markdown("- **Auxiliar:** `auxiliar` / `produccion123`")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== COLUMNA DERECHA: LOGO ==========
    with col_der:
        logo = cargar_logo()
        if logo:
            # Mostrar el logo ocupando toda la columna
            st.image(logo, use_container_width=True)
        else:
            # Si no hay logo, mostrar un huevo grande
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 400px;">
                    <span style="font-size: 180px;">🥚</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.info("💡 Sube el archivo 'logo.jpeg' o 'logo.jpg' a la raíz del repositorio para ver el logo real")
