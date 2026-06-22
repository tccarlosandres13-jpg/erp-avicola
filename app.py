# ============================================
# ERP AVICOLA - HUEVOS DOÑA DORA
# VERSIÓN CON MENÚ TIPO LIBRA (ACORDEÓN)
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
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1a0a 0%, #1a3a1a 100%) !important;
        border-right: 2px solid rgba(255,214,0,0.08) !important;
        padding: 10px 0 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* EXPANDER - ACORDEÓN */
    .streamlit-expanderHeader {
        background: rgba(255,214,0,0.06) !important;
        color: #FFD600 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 4px !important;
        border: 1px solid rgba(255,214,0,0.06) !important;
        letter-spacing: 1px !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255,214,0,0.12) !important;
        border-color: rgba(255,214,0,0.15) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.02) !important;
        border-radius: 0 0 10px 10px !important;
        padding: 4px 0 !important;
    }
    
    .sidebar-title {
        text-align: center !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #FFD600 !important;
        letter-spacing: 2px !important;
    }
    
    /* Botones de sub-módulo dentro del acordeón */
    .submenu-btn {
        background: rgba(255,255,255,0.03) !important;
        color: rgba(255,255,255,0.7) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        border: none !important;
        width: 100% !important;
        text-align: left !important;
        margin: 2px 0 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .submenu-btn:hover {
        background: rgba(255,214,0,0.08) !important;
        color: #FFD600 !important;
        padding-left: 18px !important;
    }
    
    .stAlert {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        color: rgba(255,255,255,0.7) !important;
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

# ============================================
# MENÚ ACORDEÓN (TIPO LIBRA)
# ============================================

st.sidebar.markdown("### 📋 NAVEGACIÓN")

# Diccionario de módulos por categoría
categorias = {
    "📊 MÓDULOS OPERACIONALES": [
        {"nombre": "🏦 Gestión Financiera", "key": "financiera"},
        {"nombre": "🏛️ Gestión de Bancos", "key": "bancos"},
        {"nombre": "🛒 Gestión de Compra", "key": "compras"},
        {"nombre": "🚚 Gestión de Logística", "key": "logistica"},
        {"nombre": "🔔 Gestión de Alerta", "key": "alertas"},
        {"nombre": "⚙️ Gestión de Procesos", "key": "procesos"},
    ],
    "⚙️ DISEÑO Y AUTOMATIZACIÓN": [
        {"nombre": "📇 CRM", "key": "crm"},
        {"nombre": "🛍️ Comercio Electrónico", "key": "ecommerce"},
        {"nombre": "🐔 Producción", "key": "produccion"},
        {"nombre": "💰 Gestión de Ventas", "key": "ventas"},
        {"nombre": "🧾 Factura Electrónica", "key": "facturacion"},
        {"nombre": "📺 TVP", "key": "tvp"},
    ],
    "🔧 FRAMEWORK LIBRA": [
        {"nombre": "🎨 Entorno de Personalización", "key": "personalizacion"},
        {"nombre": "👑 Líderes de Personalización", "key": "lideres"},
    ],
    "📊 EXTRACCIÓN DE DATOS": [
        {"nombre": "📋 Generación de Informes", "key": "informes"},
        {"nombre": "📊 Gestión de Informes", "key": "gestion_informes"},
    ],
    "🔗 INTEGRACIÓN": [
        {"nombre": "🌐 Servicios web 'Galileo'", "key": "galileo"},
        {"nombre": "📱 Dispositivos móviles", "key": "moviles"},
    ],
    "📱 MOVILIDAD": [
        {"nombre": "📱 Dispositivos móviles", "key": "movilidad"},
    ],
}

# Mostrar acordeones
for categoria, submodulos in categorias.items():
    with st.sidebar.expander(f"{categoria}", expanded=False):
        for sub in submodulos:
            # Botón personalizado para cada sub-módulo
            if st.button(
                f"{sub['nombre']}",
                key=f"sub_{sub['key']}",
                use_container_width=True,
                help=f"Ir a {sub['nombre']}"
            ):
                st.session_state.menu_seleccionado = sub['key']
                st.rerun()
            
            # Estilo del botón
            st.markdown(f"""
            <style>
                div[data-testid="stButton"] button[key="sub_{sub['key']}"] {{
                    background: rgba(255,255,255,0.02) !important;
                    color: rgba(255,255,255,0.6) !important;
                    border-radius: 8px !important;
                    padding: 6px 12px !important;
                    font-size: 12px !important;
                    font-weight: 500 !important;
                    border: none !important;
                    width: 100% !important;
                    text-align: left !important;
                    margin: 2px 0 !important;
                    transition: all 0.3s ease !important;
                    height: auto !important;
                    min-height: 32px !important;
                    box-shadow: none !important;
                }}
                div[data-testid="stButton"] button[key="sub_{sub['key']}"]:hover {{
                    background: rgba(255,214,0,0.08) !important;
                    color: #FFD600 !important;
                    padding-left: 18px !important;
                }}
            </style>
            """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# Botón de inicio
if st.sidebar.button("🏠 Inicio", use_container_width=True):
    st.session_state.menu_seleccionado = "inicio"
    st.rerun()

# Botón de cerrar sesión
if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
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
else:
    # Para módulos que aún no tienen funcionalidad
    st.title("🚧 Módulo en construcción")
    st.markdown("""
    <div style="
        background: rgba(255,214,0,0.05);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        border: 1px solid rgba(255,214,0,0.08);
    ">
        <div style="font-size: 48px; margin-bottom: 20px;">🔧</div>
        <div style="font-size: 24px; font-weight: 700; color: #FFD600;">Módulo en desarrollo</div>
        <div style="font-size: 14px; color: rgba(255,255,255,0.3); margin-top: 10px;">
            Estamos trabajando para traerte esta funcionalidad muy pronto.
        </div>
    </div>
    """, unsafe_allow_html=True)
