# ============================================
# ERP AVICOLA - HUEVOS DOÑA DORA
# VERSIÓN CON DISEÑO MEJORADO
# ============================================

import streamlit as st
from modulos.datos import usuarios, hash_password, cargar_logo
from modulos.login import mostrar_login
from modulos.inicio import mostrar_inicio
from modulos.produccion import mostrar_produccion
from modulos.ventas import mostrar_ventas
from modulos.inventario_huevos import mostrar_inventario_huevos
from modulos.categorias import mostrar_categorias
from modulos.reportes import mostrar_reportes
from modulos.usuarios import mostrar_usuarios
from modulos.configuracion import mostrar_configuracion

st.set_page_config(page_title="Doña Dora - ERP", page_icon="🥚", layout="wide")

st.markdown("""
<style>
    /* ====== FONDO OSCURO CON GRADIENTE ====== */
    html, body, .stApp {
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: linear-gradient(135deg, #0d1f0d 0%, #1a3a1a 50%, #2d5a2d 100%) !important;
    }
    
    .stApp > header {
        background: transparent !important;
    }
    
    .row-widget.stColumns {
        display: flex !important;
        align-items: stretch !important;
    }
    
    /* ====== SIDEBAR MEJORADA ====== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a150a 0%, #1a2a1a 100%) !important;
        border-right: 2px solid rgba(255,214,0,0.12) !important;
        padding: 15px 0 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: rgba(255,255,255,0.9) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255,255,255,0.9) !important;
    }
    
    .sidebar-title {
        text-align: center !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        color: #FFD600 !important;
        letter-spacing: 2px !important;
        text-shadow: 0 0 30px rgba(255,214,0,0.1) !important;
    }
    
    /* ====== BOTONES DEL SIDEBAR ====== */
    div[data-testid="stButton"] button {
        background: rgba(255,255,255,0.06) !important;
        color: rgba(255,255,255,0.9) !important;
        border-radius: 14px !important;
        padding: 16px 6px !important;
        height: auto !important;
        min-height: 75px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        line-height: 1.6 !important;
        white-space: pre-line !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
        text-align: center !important;
        width: 100% !important;
        color: rgba(255,255,255,0.9) !important;
    }
    
    div[data-testid="stButton"] button:hover {
        background: rgba(255,214,0,0.12) !important;
        border-color: rgba(255,214,0,0.25) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3) !important;
    }
    
    div[data-testid="stButton"] button:active {
        transform: scale(0.95) !important;
    }
    
    /* ====== TEXTO EN GENERAL ====== */
    .stMarkdown, .stText, .stTitle, .stSubheader, .stHeader {
        color: rgba(255,255,255,0.95) !important;
    }
    
    h1, h2, h3, h4, h5, h6, .stTitle, .stSubheader {
        color: #FFD600 !important;
        font-weight: 700 !important;
    }
    
    /* ====== MÉTRICAS ====== */
    [data-testid="stMetricValue"] {
        color: #FFD600 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    /* ====== INPUTS ====== */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 2px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        color: white !important;
        font-size: 15px !important;
        padding: 14px 18px !important;
        height: 55px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FFD600 !important;
        box-shadow: 0 0 30px rgba(255,214,0,0.08) !important;
        background: rgba(255,255,255,0.08) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.3) !important;
    }
    
    /* ====== BOTONES PRINCIPALES ====== */
    .stButton > button {
        background: linear-gradient(135deg, #FFD600, #F9A825) !important;
        color: #1a3a1a !important;
        border-radius: 14px !important;
        padding: 14px 24px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 6px 25px rgba(255,214,0,0.25) !important;
        transition: all 0.3s ease !important;
        height: 55px !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 40px rgba(255,214,0,0.35) !important;
    }
    
    /* ====== BOTONES DE REGRESO ====== */
    .stButton > button[key*="back"] {
        background: rgba(255,255,255,0.06) !important;
        color: rgba(255,255,255,0.8) !important;
        box-shadow: none !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }
    
    .stButton > button[key*="back"]:hover {
        background: rgba(255,214,0,0.08) !important;
        border-color: rgba(255,214,0,0.2) !important;
    }
    
    /* ====== EXPANDER ====== */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        color: rgba(255,255,255,0.7) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }
    
    .streamlit-expanderHeader:hover {
        color: #FFD600 !important;
        background: rgba(255,214,0,0.04) !important;
    }
    
    /* ====== TABLAS ====== */
    .stDataFrame, .stTable {
        background: rgba(255,255,255,0.02) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
        color: rgba(255,255,255,0.9) !important;
    }
    
    .stDataFrame th, .stDataFrame td {
        color: rgba(255,255,255,0.9) !important;
        font-size: 14px !important;
    }
    
    .stDataFrame th {
        color: #FFD600 !important;
        font-weight: 700 !important;
    }
    
    /* ====== ALERTAS ====== */
    .stAlert {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        color: rgba(255,255,255,0.8) !important;
    }
    
    .stAlert svg {
        fill: #FFD600 !important;
    }
    
    /* ====== TARJETAS DE ESTADÍSTICAS ====== */
    .summary-card {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 18px !important;
        padding: 20px 24px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        transition: all 0.3s ease !important;
    }
    
    .summary-card:hover {
        background: rgba(255,255,255,0.06) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2) !important;
    }
    
    .summary-number {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #FFD600 !important;
    }
    
    .summary-label {
        font-size: 13px !important;
        color: rgba(255,255,255,0.4) !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
    }
    
    /* ====== FILAS DE PRODUCCIÓN ====== */
    .produccion-item {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        margin-bottom: 4px !important;
        border-left: 3px solid #FFD600 !important;
        color: rgba(255,255,255,0.8) !important;
    }
    
    .produccion-item strong {
        color: #FFD600 !important;
    }
    
    /* ====== INPUTS NUMÉRICOS ====== */
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 15px !important;
        padding: 12px 16px !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #FFD600 !important;
        box-shadow: 0 0 30px rgba(255,214,0,0.05) !important;
    }
    
    /* ====== SELECTBOX ====== */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        color: white !important;
    }
    
    .stSelectbox > div > div > div {
        color: rgba(255,255,255,0.8) !important;
    }
    
    /* ====== FECHA ====== */
    .stDateInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* ====== DIVISORES ====== */
    hr {
        border-color: rgba(255,255,255,0.06) !important;
        margin: 20px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ESTADO DE SESIÓN
# ============================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

if 'menu_seleccionado' not in st.session_state:
    st.session_state.menu_seleccionado = "inicio"

if not st.session_state.logged_in:
    mostrar_login()
    st.stop()

# ============================================
# MENÚ LATERAL
# ============================================

usuario_actual = st.session_state.usuario
rol_actual = st.session_state.rol

logo = cargar_logo()
if logo:
    st.sidebar.image(logo, width=80)
else:
    st.sidebar.markdown('<p style="font-size:40px;text-align:center;">🥚</p>', unsafe_allow_html=True)

st.sidebar.markdown('<p class="sidebar-title">HUEVOS DOÑA DORA</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.write(f"**👤 Usuario:** {usuario_actual}")
st.sidebar.write(f"**🎯 Rol:** {rol_actual}")
st.sidebar.markdown("---")

# ========== BOTONES DEL MENÚ ==========
st.sidebar.markdown("### 📋 Navegación")

opciones = [
    ("🏠", "Inicio", "inicio"),
    ("🐔", "Producción", "produccion"),
    ("💰", "Ventas", "ventas"),
    ("📦", "Inventario", "inventario"),
    ("🏷️", "Categorías", "categorias"),
    ("📊", "Reportes", "reportes"),
    ("👥", "Usuarios", "usuarios"),
    ("⚙️", "Configuración", "configuracion")
]

if rol_actual != "admin":
    opciones = [o for o in opciones if o[1] not in ["Configuración", "Usuarios"]]

cols = st.sidebar.columns(2)
for i, (icono, nombre, key) in enumerate(opciones):
    with cols[i % 2]:
        if st.button(f"{icono}\n{nombre}", key=f"menu_{key}", use_container_width=True):
            st.session_state.menu_seleccionado = key
            st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.logged_in = False
    st.session_state.usuario = None
    st.rerun()

# ============================================
# NAVEGACIÓN
# ============================================

key = st.session_state.menu_seleccionado

if key == "inicio":
    mostrar_inicio()
elif key == "produccion":
    mostrar_produccion()
elif key == "ventas":
    mostrar_ventas()
elif key == "inventario":
    mostrar_inventario_huevos()
elif key == "categorias":
    mostrar_categorias()
elif key == "reportes":
    mostrar_reportes()
elif key == "usuarios":
    mostrar_usuarios()
elif key == "configuracion":
    mostrar_configuracion()
