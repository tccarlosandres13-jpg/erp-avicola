# ============================================
# ERP AVICOLA - HUEVOS DOÑA DORA
# VERSIÓN MODULAR
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password
from modulos.login import mostrar_login
from modulos.dashboard import mostrar_dashboard
from modulos.produccion import mostrar_produccion
from modulos.inventario_huevos import mostrar_inventario_huevos
from modulos.categorias import mostrar_categorias
from modulos.reportes import mostrar_reportes
from modulos.usuarios import mostrar_usuarios
from modulos.configuracion import mostrar_configuracion

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================

st.set_page_config(page_title="Doña Dora - ERP", page_icon="🥚", layout="wide")

# ============================================
# CSS PERSONALIZADO
# ============================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%);
    }
    
    .login-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #FFD600;
    }
    
    .dora-title {
        text-align: center;
        color: #2E7D32;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .dora-subtitle {
        text-align: center;
        color: #F9A825;
        font-size: 1rem;
        margin-bottom: 30px;
        font-weight: bold;
    }
    
    .stButton > button {
        background-color: #2E7D32;
        color: white;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #F9A825;
        color: #2E7D32;
    }
    
    .stButton > button[key*="back"] {
        background-color: #F9A825;
        color: #2E7D32;
    }
    
    .stButton > button[key*="back"]:hover {
        background-color: #E07B00;
        color: white;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #FFD600;
        padding: 8px 15px;
        font-size: 14px;
    }
    
    [data-testid="stMetricValue"] {
        color: #2E7D32;
    }
    
    .summary-card {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border-left: 5px solid #2E7D32;
    }
    
    .summary-number {
        font-size: 24px;
        font-weight: bold;
        color: #2E7D32;
    }
    
    .summary-label {
        font-size: 12px;
        color: #666;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2E7D32 0%, #1B5E20 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .sidebar-title {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #FFD600 !important;
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
# MENÚ PRINCIPAL (después del login)
# ============================================

usuario_actual = st.session_state.usuario
rol_actual = st.session_state.rol

# Logo en la sidebar
from modulos.datos import cargar_logo
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

# Menú según el rol
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
# NAVEGACIÓN ENTRE MÓDULOS
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
