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
        padding: 25px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #FFD600;
        height: 100%;
        min-height: 520px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* TÍTULO CON ESTILO GEO */
    .dora-title-geo {
        text-align: center;
        color: #2E7D32;
        font-size: 1.6rem;
        font-weight: 900;
        margin-bottom: 5px;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-family: 'Arial Black', 'Impact', sans-serif;
        text-shadow: 2px 2px 0px rgba(249, 168, 37, 0.3);
    }
    
    .dora-subtitle {
        text-align: center;
        color: #F9A825;
        font-size: 0.8rem;
        margin-bottom: 20px;
        font-weight: bold;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    /* CAMPOS DE TEXTO MÁS PEQUEÑOS */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #FFD600;
        padding: 5px 12px;
        font-size: 12px;
        height: 35px;
        background-color: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E7D32;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.2);
    }
    
    /* BOTONES */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32, #388E3C);
        color: white;
        border-radius: 25px;
        padding: 7px 18px;
        font-weight: bold;
        font-size: 13px;
        border: none;
        width: 100%;
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.3);
        transition: all 0.3s ease;
        height: 38px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #F9A825, #FFC107);
        color: #2E7D32;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(249, 168, 37, 0.4);
    }
    
    .stButton > button[key*="back"] {
        background: linear-gradient(135deg, #F9A825, #FFC107);
        color: #2E7D32;
    }
    
    .stButton > button[key*="back"]:hover {
        background: linear-gradient(135deg, #E07B00, #F9A825);
        color: white;
    }
    
    /* MÉTRICAS */
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
    
    /* SIDEBAR */
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
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background-color: rgba(46, 125, 50, 0.05);
        border-radius: 12px;
        font-weight: 600;
        color: #2E7D32;
        font-size: 13px;
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
