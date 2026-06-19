# ============================================
# ERP AVICOLA - HUEVOS DOÑA DORA
# VERSIÓN MODULAR COMPLETA
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
from modulos.login import mostrar_login
from modulos.dashboard import mostrar_dashboard
from modulos.produccion import mostrar_produccion
from modulos.inventario_huevos import mostrar_inventario_huevos
from modulos.categorias import mostrar_categorias
from modulos.reportes import mostrar_reportes
from modulos.usuarios import mostrar_usuarios
from modulos.configuracion import mostrar_configuracion

st.set_page_config(page_title="Doña Dora - ERP", page_icon="🥚", layout="wide")

st.markdown("""
<style>
    html, body, .stApp {
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%);
    }
    
    .stApp > header {
        background: transparent !important;
    }
    
    /* COLUMNAS AL 100% */
    .row-widget.stColumns {
        height: 100vh !important;
        min-height: 100vh !important;
        max-height: 100vh !important;
        display: flex !important;
        align-items: stretch !important;
    }
    
    .row-widget.stColumns > div {
        height: 100vh !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* CAMPOS DE TEXTO */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #E0E0E0 !important;
        padding: 10px 16px !important;
        font-size: 14px !important;
        height: 48px !important;
        background-color: #F8F9FA !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E7D32 !important;
        box-shadow: 0 0 0 4px rgba(46, 125, 50, 0.08) !important;
        background-color: white !important;
    }
    
    /* BOTÓN */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32, #388E3C) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.25) !important;
        transition: all 0.3s ease !important;
        height: 48px !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1B5E20, #2E7D32) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(46, 125, 50, 0.35) !important;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%) !important;
        border-right: 3px solid #FFD600 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 6px !important;
    }
    
    .sidebar-title {
        text-align: center !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #FFD600 !important;
    }
    
    /* TARJETAS */
    .summary-card {
        background: white !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
        border-left: 5px solid #2E7D32 !important;
    }
    
    .summary-number {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #2E7D32 !important;
    }
    
    .summary-label {
        font-size: 13px !important;
        color: #777 !important;
        font-weight: 500 !important;
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background: transparent !important;
        color: #2E7D32 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border-bottom: 1px dashed #E0E0E0 !important;
        border-radius: 0 !important;
        padding: 8px 0 !important;
        justify-content: center !important;
    }
    
    .streamlit-expanderHeader:hover {
        color: #F9A825 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOGIN
# ============================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

if not st.session_state.logged_in:
    mostrar_login()
    st.stop()

# ============================================
# MENÚ PRINCIPAL
# ============================================

usuario_actual = st.session_state.usuario
rol_actual = st.session_state.rol

logo = cargar_logo()
if logo:
    st.sidebar.image(logo, width=80)
else:
    st.sidebar.markdown('<p style="font-size: 40px; text-align: center;">🥚</p>', unsafe_allow_html=True)

st.sidebar.markdown('<p class="sidebar-title">HUEVOS DOÑA DORA</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.write(f"**Usuario:** {usuario_actual}")
st.sidebar.write(f"**Rol:** {rol_actual}")
st.sidebar.write("---")

if rol_actual == "admin":
    menu = st.sidebar.radio("📋 Menú Principal", [
        "🏠 Dashboard",
        "🐔 Producción",
        "📦 Inventario Huevos",
        "🏷️ Categorías",
        "📊 Reportes",
        "👥 Usuarios",
        "⚙️ Configuración"
    ])
else:
    menu = st.sidebar.radio("📋 Menú Principal", [
        "🏠 Dashboard",
        "🐔 Producción",
        "📦 Inventario Huevos",
        "📊 Reportes"
    ])

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.logged_in = False
    st.session_state.usuario = None
    st.rerun()

# ============================================
# NAVEGACIÓN
# ============================================

if menu == "🏠 Dashboard":
    mostrar_dashboard()
elif menu == "🐔 Producción":
    mostrar_produccion()
elif menu == "📦 Inventario Huevos":
    mostrar_inventario_huevos()
elif menu == "🏷️ Categorías":
    mostrar_categorias()
elif menu == "📊 Reportes":
    mostrar_reportes()
elif menu == "👥 Usuarios":
    mostrar_usuarios()
elif menu == "⚙️ Configuración":
    mostrar_configuracion()
