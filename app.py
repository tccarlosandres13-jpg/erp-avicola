# ============================================
# ERP AVICOLA - HUEVOS DOÑA DORA
# VERSIÓN CORREGIDA
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
    html, body, .stApp {
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: linear-gradient(135deg, #0a1a0a 0%, #1a3a1a 40%, #2d5a2d 100%) !important;
    }
    
    .stApp > header {
        background: transparent !important;
    }
    
    .row-widget.stColumns {
        display: flex !important;
        align-items: stretch !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1a0a 0%, #1a3a1a 100%) !important;
        border-right: 2px solid rgba(255,214,0,0.08) !important;
        padding: 10px 0 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .sidebar-title {
        text-align: center !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #FFD600 !important;
        letter-spacing: 2px !important;
    }
    
    .stAlert {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        color: rgba(255,255,255,0.7) !important;
    }
    
    /* Botones del menú lateral */
    div[data-testid="stButton"] button {
        background: rgba(255,255,255,0.04) !important;
        color: white !important;
        border-radius: 14px !important;
        padding: 14px 4px !important;
        height: auto !important;
        min-height: 70px !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        line-height: 1.6 !important;
        white-space: pre-line !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    div[data-testid="stButton"] button:hover {
        background: rgba(255,214,0,0.08) !important;
        border-color: rgba(255,214,0,0.2) !important;
        transform: translateY(-3px) !important;
    }
    
    div[data-testid="stButton"] button:active {
        transform: scale(0.95) !important;
    }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

if 'menu_seleccionado' not in st.session_state:
    st.session_state.menu_seleccionado = "inicio"

if not st.session_state.logged_in:
    mostrar_login()
    st.stop()

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

# ========== MENÚ CON BOTONES ==========
st.sidebar.markdown("### 📋 Navegación")

# Opciones del menú
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

# Mostrar en grid 2x2
cols = st.sidebar.columns(2)
for i, (icono, nombre, key) in enumerate(opciones):
    with cols[i % 2]:
        if st.button(
            f"{icono}\n{nombre}",
            key=f"menu_{key}",
            use_container_width=True,
            help=f"Ir a {nombre}"
        ):
            st.session_state.menu_seleccionado = key
            st.rerun()

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
