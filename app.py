# ============================================
# ERP AVICOLA - HUEVOS DOÑA DORA
# VERSIÓN MODULAR CON DISEÑO MEJORADO
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

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================

st.set_page_config(page_title="Doña Dora - ERP", page_icon="🥚", layout="wide")

# ============================================
# CSS PERSONALIZADO - DISEÑO MEJORADO
# ============================================

st.markdown("""
<style>
    /* FONDO GENERAL */
    .stApp {
        background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%);
    }
    
    /* TARJETA DE LOGIN */
    .login-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #FFD600;
        backdrop-filter: blur(10px);
    }
    
    /* TÍTULOS */
    .dora-title {
        text-align: center;
        color: #2E7D32;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .dora-subtitle {
        text-align: center;
        color: #F9A825;
        font-size: 1rem;
        margin-bottom: 30px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    /* BOTONES PRINCIPALES */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32, #388E3C);
        color: white;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        border: none;
        width: 100%;
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #F9A825, #FFC107);
        color: #2E7D32;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(249, 168, 37, 0.4);
    }
    
    /* BOTÓN REGRESAR */
    .stButton > button[key*="back"] {
        background: linear-gradient(135deg, #F9A825, #FFC107);
        color: #2E7D32;
    }
    
    .stButton > button[key*="back"]:hover {
        background: linear-gradient(135deg, #E07B00, #F9A825);
        color: white;
    }
    
    /* INPUTS */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #FFD600;
        padding: 10px 18px;
        font-size: 14px;
        background-color: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E7D32;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.2);
    }
    
    /* MÉTRICAS DASHBOARD */
    [data-testid="stMetricValue"] {
        color: #2E7D32;
        font-size: 2rem !important;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #555;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        color: #F9A825;
    }
    
    /* TARJETAS DE RESUMEN */
    .summary-card {
        background: white;
        border-radius: 15px;
        padding: 18px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #2E7D32;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .summary-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .summary-number {
        font-size: 28px;
        font-weight: bold;
        color: #2E7D32;
        line-height: 1.2;
    }
    
    .summary-label {
        font-size: 13px;
        color: #777;
        margin-top: 5px;
        font-weight: 500;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2E7D32 0%, #1B5E20 100%);
        border-right: 3px solid #FFD600;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 8px;
    }
    
    [data-testid="stSidebar"] .stRadio > div:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-title {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #FFD600 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* TABLAS */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background-color: rgba(46, 125, 50, 0.05);
        border-radius: 12px;
        font-weight: 600;
        color: #2E7D32;
    }
    
    /* BOTONES DE ACCIÓN EN PRODUCCIÓN */
    .action-buttons .stButton > button {
        background: white;
        color: #2E7D32;
        border: 2px solid #2E7D32;
        box-shadow: none;
    }
    
    .action-buttons .stButton > button:hover {
        background: #2E7D32;
        color: white;
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

logo = cargar_logo()
if logo:
    st.sidebar.image(logo, width=80)
else:
    st.sidebar.markdown('<p style="font-size: 40px; text-align: center;">🥚</p>', unsafe_allow_html=True)

st.sidebar.markdown('<p class="sidebar-title">HUEVOS DOÑA DORA</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.write(f"**👤 Usuario:** {usuario_actual}")
st.sidebar.write(f"**🎯 Rol:** {rol_actual}")
st.sidebar.markdown("---")

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
