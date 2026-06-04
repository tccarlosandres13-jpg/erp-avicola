# ============================================
# ERP AVICOLA - HUEVOS DOÑA DORA
# Versión 2.1 - Con Inventario de Gallinas
# ============================================

import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import json
import os
from PIL import Image

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================

st.set_page_config(
    page_title="Doña Dora - ERP", 
    page_icon="🥚", 
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO (Colores Verde y Amarillo)
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
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #FFD600;
        padding: 8px 15px;
        font-size: 14px;
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
    
    [data-testid="stMetricValue"] {
        color: #2E7D32;
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 20px;
        padding: 8px 20px;
        background-color: #E8F5E9;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2E7D32 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIÓN PARA CARGAR EL LOGO
# ============================================

def cargar_logo():
    logo_path = "logo.jpeg"
    if os.path.exists(logo_path):
        return Image.open(logo_path)
    else:
        logo_path_jpg = "logo.jpg"
        if os.path.exists(logo_path_jpg):
            return Image.open(logo_path_jpg)
    return None

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

USUARIOS_FILE = 'usuarios.json'
GALPONES_FILE = 'galpones.json'
PRODUCCION_FILE = 'produccion.json'
INVENTARIO_HUEVOS_FILE = 'inventario.json'
CATEGORIAS_FILE = 'categorias.json'
INVENTARIO_GALLINAS_FILE = 'inventario_gallinas.json'
MOVIMIENTOS_GALLINAS_FILE = 'movimientos_gallinas.json'

def cargar_datos(archivo, por_defecto):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return por_defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Datos por defecto
USUARIOS_POR_DEFECTO = {
    "admin": {
        "password": hash_password("admin123"),
        "nombre": "Administrador",
        "rol": "admin"
    },
    "auxiliar": {
        "password": hash_password("produccion123"),
        "nombre": "Auxiliar de Producción",
        "rol": "produccion"
    }
}

GALPONES_POR_DEFECTO = [
    {"id": 1, "nombre": "Galpón 1", "cantidad_gallinas": 75000, "estado": "produccion"},
    {"id": 2, "nombre": "Galpón 2", "cantidad_gallinas": 0, "estado": "mantenimiento"},
    {"id": 3, "nombre": "Galpón 3", "cantidad_gallinas": 25000, "estado": "produccion"},
    {"id": 4, "nombre": "Galpón Levante", "cantidad_gallinas": 0, "estado": "descanso"}
]

CATEGORIAS_POR_DEFECTO = {
    "categorias": ["Extra", "AAA", "AA", "A", "B"],
    "editable": True
}

INVENTARIO_GALLINAS_POR_DEFECTO = {}

MOVIMIENTOS_GALLINAS_POR_DEFECTO = []

# Cargar datos
usuarios = cargar_datos(USUARIOS_FILE, USUARIOS_POR_DEFECTO)
galpones = cargar_datos(GALPONES_FILE, GALPONES_POR_DEFECTO)
produccion = cargar_datos(PRODUCCION_FILE, [])
inventario_huevos = cargar_datos(INVENTARIO_HUEVOS_FILE, {})
categorias_data = cargar_datos(CATEGORIAS_FILE, CATEGORIAS_POR_DEFECTO)
inventario_gallinas = cargar_datos(INVENTARIO_GALLINAS_FILE, INVENTARIO_GALLINAS_POR_DEFECTO)
movimientos_gallinas = cargar_datos(MOVIMIENTOS_GALLINAS_FILE, MOVIMIENTOS_GALLINAS_POR_DEFECTO)

# Inicializar inventario de gallinas con los datos de galpones
if not inventario_gallinas:
    for g in galpones:
        inventario_gallinas[str(g["id"])] = {
            "nombre": g["nombre"],
            "cantidad": g["cantidad_gallinas"],
            "estado": g["estado"]
        }
    guardar_datos(INVENTARIO_GALLINAS_FILE, inventario_gallinas)

# Inicializar inventario de huevos
if not inventario_huevos:
    for cat in categorias_data["categorias"]:
        inventario_huevos[f"Bodega1_{cat}"] = 0
    inventario_huevos["Bodega1_total"] = 0
    guardar_datos(INVENTARIO_HUEVOS_FILE, inventario_huevos)

# ============================================
# FUNCIONES DE GALLINAS
# ============================================

def registrar_movimiento_gallinas(galpon_id, tipo_movimiento, cantidad, motivo, fecha):
    """Registra un movimiento de gallinas (mortalidad, levante, descarte)"""
    galpon = next((g for g in galpones if g["id"] == galpon_id), None)
    if not galpon:
        return False, "Galpón no encontrado"
    
    # Obtener cantidad actual
    cantidad_actual = inventario_gallinas.get(str(galpon_id), {}).get("cantidad", 0)
    
    if tipo_movimiento == "mortalidad":
        nueva_cantidad = cantidad_actual - cantidad
        if nueva_cantidad < 0:
            return False, "No se puede registrar mortalidad mayor a las gallinas existentes"
    elif tipo_movimiento == "levante":
        nueva_cantidad = cantidad_actual + cantidad
    elif tipo_movimiento == "descarte":
        nueva_cantidad = cantidad_actual - cantidad
        if nueva_cantidad < 0:
            return False, "No se puede registrar descarte mayor a las gallinas existentes"
    else:
        return False, "Tipo de movimiento no válido"
    
    # Guardar movimiento
    movimiento = {
        "id": len(movimientos_gallinas) + 1,
        "galpon_id": galpon_id,
        "galpon_nombre": galpon["nombre"],
        "fecha": fecha,
        "tipo": tipo_movimiento,
        "cantidad": cantidad,
        "motivo": motivo,
        "cantidad_anterior": cantidad_actual,
        "cantidad_nueva": nueva_cantidad
    }
    movimientos_gallinas.append(movimiento)
    guardar_datos(MOVIMIENTOS_GALLINAS_FILE, movimientos_gallinas)
    
    # Actualizar inventario
    inventario_gallinas[str(galpon_id)] = {
        "nombre": galpon["nombre"],
        "cantidad": nueva_cantidad,
        "estado": galpon["estado"]
    }
    guardar_datos(INVENTARIO_GALLINAS_FILE, inventario_gallinas)
    
    # Actualizar galpones
    for g in galpones:
        if g["id"] == galpon_id:
            g["cantidad_gallinas"] = nueva_cantidad
            break
    guardar_datos(GALPONES_FILE, galpones)
    
    return True, movimiento

# ============================================
# FUNCIONES DE PRODUCCIÓN DE HUEVOS
# ============================================

def registrar_produccion(galpon_id, fecha, clasificacion):
    nuevo_registro = {
        "id": len(produccion) + 1,
        "galpon_id": galpon_id,
        "fecha": fecha,
        "clasificacion": clasificacion,
        "total_huevos": sum(clasificacion.values())
    }
    produccion.append(nuevo_registro)
    guardar_datos(PRODUCCION_FILE, produccion)
    
    for categoria, cantidad in clasificacion.items():
        inventario_huevos[f"Bodega1_{categoria}"] = inventario_huevos.get(f"Bodega1_{categoria}", 0) + cantidad
        inventario_huevos["Bodega1_total"] = inventario_huevos.get("Bodega1_total", 0) + cantidad
    guardar_datos(INVENTARIO_HUEVOS_FILE, inventario_huevos)
    return nuevo_registro

def agregar_categoria(nueva_categoria):
    if nueva_categoria and nueva_categoria not in categorias_data["categorias"]:
        categorias_data["categorias"].append(nueva_categoria)
        guardar_datos(CATEGORIAS_FILE, categorias_data)
        inventario_huevos[f"Bodega1_{nueva_categoria}"] = 0
        guardar_datos(INVENTARIO_HUEVOS_FILE, inventario_huevos)
        return True
    return False

def eliminar_categoria(categoria):
    if categoria in categorias_data["categorias"] and categoria not in ["Extra", "AAA", "AA", "A", "B"]:
        if inventario_huevos.get(f"Bodega1_{categoria}", 0) == 0:
            categorias_data["categorias"].remove(categoria)
            guardar_datos(CATEGORIAS_FILE, categorias_data)
            return True
    return False

# ============================================
# INTERFAZ DE LOGIN
# ============================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        logo = cargar_logo()
        if logo:
            st.image(logo, width=150, use_container_width=False)
        else:
            st.markdown('<div style="text-align: center;"><span style="font-size: 100px;">🥚</span></div>', unsafe_allow_html=True)
        
        st.markdown('<h1 class="dora-title">HUEVOS DOÑA DORA</h1>', unsafe_allow_html=True)
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
            st.markdown("- **Administrador:** `admin` / `admin123`\n- **Auxiliar:** `auxiliar` / `produccion123`")
        
        st.markdown('</div>', unsafe_allow_html=True)
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
# MÓDULO: DASHBOARD
# ============================================
if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard - Resumen del Día")
    
    col1, col2, col3, col4 = st.columns(4)
    
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    
    total_inventario = inventario_huevos.get("Bodega1_total", 0)
    
    # Total gallinas vivas
    total_gallinas = sum(g.get("cantidad", 0) for g in inventario_gallinas.values())
    
    # Mortalidad del mes
    mes_actual = datetime.now().strftime("%Y-%m")
    mortalidad_mes = sum(m["cantidad"] for m in movimientos_gallinas 
                         if m["tipo"] == "mortalidad" and m["fecha"].startswith(mes_actual))
    
    col1.metric("🥚 Producción Hoy", f"{total_hoy:,} huevos")
    col2.metric("📦 Inventario Bodega 1", f"{total_inventario:,} huevos")
    col3.metric("🐔 Gallinas Vivas", f"{total_gallinas:,}")
    col4.metric("⚠️ Mortalidad (mes)", f"{mortalidad_mes:,}")
    
    st.write("---")
    st.subheader("📈 Últimas Producciones")
    if produccion:
        ultimas = produccion[-5:][::-1]
        for p in ultimas:
            galpon_nombre = next((g["nombre"] for g in galpones if g["id"] == p["galpon_id"]), "Desconocido")
            st.write(f"**{p['fecha']} - {galpon_nombre}**: {p['total_huevos']:,} huevos")
    else:
        st.info("No hay registros de producción aún.")

# ============================================
# MÓDULO: PRODUCCIÓN (AHORA CON INVENTARIO DE GALLINAS)
# ============================================
elif menu == "🐔 Producción":
    st.title("🐔 Gestión de Producción")
    
    # Crear pestañas dentro de Producción
    tab1, tab2, tab3 = st.tabs(["📝 Registrar Producción", "🐔 Inventario de Gallinas", "📜 Historial de Gallinas"])
    
    # ==================== TAB 1: REGISTRAR PRODUCCIÓN ====================
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            galpones_activos = [g for g in galpones if g["estado"] == "produccion" and g["cantidad_gallinas"] > 0]
            if not galpones_activos:
                st.warning("⚠️ No hay galpones activos con gallinas. Registra ingreso de levante en 'Inventario de Gallinas'.")
            else:
                galpon_seleccionado = st.selectbox(
                    "Seleccione el galpón",
                    galpones_activos,
                    format_func=lambda x: f"{x['nombre']} ({x['cantidad_gallinas']:,} gallinas)"
                )
                
                fecha = st.date_input("Fecha de producción", datetime.now())
                
                # Mostrar producción esperada (90% de postura)
                gallinas_galpon = galpon_seleccionado["cantidad_gallinas"]
                produccion_esperada = int(gallinas_galpon * 0.9)
                st.info(f"📊 Producción esperada (90%): {produccion_esperada:,} huevos")
                
                st.write("---")
                st.subheader("Clasificación de huevos")
                
                clasificacion = {}
                cols = st.columns(2)
                for i, cat in enumerate(categorias_data["categorias"]):
                    with cols[i % 2]:
                        clasificacion[cat] = st.number_input(f"{cat}", min_value=0, value=0, step=100)
                
                total_ingresado = sum(clasificacion.values())
                st.info(f"📊 Total de huevos a registrar: {total_ingresado:,}")
                
                if total_ingresado > produccion_esperada * 1.1:
                    st.warning("⚠️ La producción ingresada es mayor al 110% de lo esperado. Verifica los números.")
                
                if st.button("✅ Registrar Producción", type="primary"):
                    if total_ingresado > 0:
                        clasificacion_filtrada = {k: v for k, v in clasificacion.items() if v > 0}
                        registrar_produccion(
                            galpon_seleccionado["id"],
                            fecha.strftime("%Y-%m-%d"),
                            clasificacion_filtrada
                        )
                        st.success(f"✅ Producción registrada: {total_ingresado:,} huevos")
                        st.rerun()
                    else:
                        st.error("❌ Debe ingresar al menos un huevo")
        
        with col2:
            st.subheader("📋 Instrucciones")
            st.write("""
            1. Selecciona el **galpón** que terminó de recolectar
            2. Ingresa la **fecha** (hoy por defecto)
            3. Anota los números que salen en la **clasificadora**
            4. Completa cada categoría (Extra, AAA, etc.)
            5. Presiona **Registrar Producción**
            
            > ℹ️ El sistema sumará automáticamente al inventario de **Bodega 1**
            """)
            
            st.write("---")
            st.subheader("📈 Producción de Hoy")
            hoy = datetime.now().strftime("%Y-%m-%d")
            produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
            if produccion_hoy:
                for p in produccion_hoy:
                    galpon = next((g["nombre"] for g in galpones if g["id"] == p["galpon_id"]), "?")
                    st.write(f"**{galpon}**: {p['total_huevos']:,} huevos")
    
    # ==================== TAB 2: INVENTARIO DE GALLINAS ====================
    with tab2:
        st.subheader("🐔 Estado actual de galpones")
        
        # Mostrar tabla de inventario actual
        datos_galpones = []
        for g in galpones:
            cantidad_actual = inventario_gallinas.get(str(g["id"]), {}).get("cantidad", 0)
            datos_galpones.append({
                "Galpón": g["nombre"],
                "Gallinas actuales": f"{cantidad_actual:,}",
                "Estado": g["estado"],
                "Capacidad máxima": "100,000" if "Levante" not in g["nombre"] else "50,000"
            })
        
        st.dataframe(pd.DataFrame(datos_galpones), use_container_width=True)
        
        st.write("---")
        st.subheader("📝 Registrar movimiento de gallinas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            galpon_mov = st.selectbox(
                "Seleccione el galpón",
                galpones,
                format_func=lambda x: f"{x['nombre']} - Actual: {inventario_gallinas.get(str(x['id']), {}).get('cantidad', 0):,} gallinas",
                key="galpon_mov"
            )
            
            tipo_movimiento = st.selectbox(
                "Tipo de movimiento",
                ["levante", "mortalidad", "descarte"],
                format_func=lambda x: {
                    "levante": "➕ Ingreso de levante (nuevas gallinas)",
                    "mortalidad": "⚠️ Mortalidad (gallinas muertas)",
                    "descarte": "📤 Descarte (gallinas retiradas)"
                }.get(x, x)
            )
        
        with col2:
            cantidad_mov = st.number_input("Cantidad de gallinas", min_value=1, value=1, step=10)
            
            motivos = {
                "levante": ["Llegada de pollitas", "Traslado desde levante", "Compra de aves"],
                "mortalidad": ["Enfermedad", "Golpe de calor", "Canibalismo", "Problema respiratorio", "Otra causa"],
                "descarte": ["Fin de ciclo", "Baja producción", "Enfermedad crónica", "Renovación de lote"]
            }
            
            motivo = st.selectbox("Motivo", motivos.get(tipo_movimiento, ["Otro"]))
            
            motivo_extra = st.text_input("Observaciones adicionales (opcional)", placeholder="Detalles específicos...")
            motivo_completo = motivo + (f" - {motivo_extra}" if motivo_extra else "")
        
        fecha_mov = st.date_input("Fecha del movimiento", datetime.now())
        
        if st.button("✅ Registrar movimiento", type="primary"):
            cantidad_actual = inventario_gallinas.get(str(galpon_mov["id"]), {}).get("cantidad", 0)
            
            if tipo_movimiento == "mortalidad" and cantidad_mov > cantidad_actual:
                st.error(f"❌ No hay suficientes gallinas. Actualmente hay {cantidad_actual:,} gallinas.")
            elif tipo_movimiento == "descarte" and cantidad_mov > cantidad_actual:
                st.error(f"❌ No hay suficientes gallinas. Actualmente hay {cantidad_actual:,} gallinas.")
            else:
                success, resultado = registrar_movimiento_gallinas(
                    galpon_mov["id"],
                    tipo_movimiento,
                    cantidad_mov,
                    motivo_completo,
                    fecha_mov.strftime("%Y-%m-%d")
                )
                
                if success:
                    if tipo_movimiento == "levante":
                        st.success(f"✅ {cantidad_mov:,} gallinas ingresadas a {galpon_mov['nombre']}")
                    elif tipo_movimiento == "mortalidad":
                        st.warning(f"⚠️ {cantidad_mov:,} gallinas registradas como mortalidad en {galpon_mov['nombre']}")
                    else:
                        st.info(f"📤 {cantidad_mov:,} gallinas descartadas de {galpon_mov['nombre']}")
                    st.rerun()
                else:
                    st.error(f"❌ {resultado}")
    
    # ==================== TAB 3: HISTORIAL DE GALLINAS ====================
    with tab3:
        st.subheader("📜 Historial de movimientos de gallinas")
        
        if movimientos_gallinas:
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                tipos = ["Todos"] + list(set(m["tipo"] for m in movimientos_gallinas))
                filtro_tipo = st.selectbox("Filtrar por tipo", tipos)
            with col2:
                fechas = sorted(set(m["fecha"] for m in movimientos_gallinas), reverse=True)
                filtro_fecha = st.selectbox("Filtrar por fecha", ["Todas"] + fechas)
            
            # Filtrar datos
            movimientos_filtrados = movimientos_gallinas.copy()
            if filtro_tipo != "Todos":
                movimientos_filtrados = [m for m in movimientos_filtrados if m["tipo"] == filtro_tipo]
            if filtro_fecha != "Todas":
                movimientos_filtrados = [m for m in movimientos_filtrados if m["fecha"] == filtro_fecha]
            
            # Mostrar tabla
            df_movimientos = pd.DataFrame(movimientos_filtrados[::-1])
            df_movimientos["tipo_icono"] = df_movimientos["tipo"].map({
                "levante": "➕", "mortalidad": "⚠️", "descarte": "📤"
            })
            df_mostrar = df_movimientos[["fecha", "tipo_icono", "galpon_nombre", "cantidad", "motivo", "cantidad_anterior", "cantidad_nueva"]]
            df_mostrar.columns = ["Fecha", " ", "Galpón", "Cantidad", "Motivo", "Anterior", "Nueva"]
            st.dataframe(df_mostrar, use_container_width=True)
            
            # Resumen estadístico
            st.write("---")
            st.subheader("📊 Resumen de movimientos")
            
            col1, col2, col3 = st.columns(3)
            total_levante = sum(m["cantidad"] for m in movimientos_gallinas if m["tipo"] == "levante")
            total_mortalidad = sum(m["cantidad"] for m in movimientos_gallinas if m["tipo"] == "mortalidad")
            total_descarte = sum(m["cantidad"] for m in movimientos_gallinas if m["tipo"] == "descarte")
            
            col1.metric("➕ Total Levante", f"{total_levante:,}")
            col2.metric("⚠️ Total Mortalidad", f"{total_mortalidad:,}")
            col3.metric("📤 Total Descarte", f"{total_descarte:,}")
        else:
            st.info("No hay movimientos registrados aún. Usa 'Inventario de Gallinas' para registrar ingresos o mortalidad.")

# ============================================
# MÓDULO: INVENTARIO HUEVOS
# ============================================
elif menu == "📦 Inventario Huevos":
    st.title("📦 Inventario - Bodega 1 (Granja San Miguel)")
    
    total = inventario_huevos.get("Bodega1_total", 0)
    st.metric("Total de huevos en bodega", f"{total:,}")
    
    st.write("---")
    st.subheader("📊 Detalle por categoría")
    
    datos_inventario = []
    for cat in categorias_data["categorias"]:
        cantidad = inventario_huevos.get(f"Bodega1_{cat}", 0)
        if cantidad > 0 or total > 0:
            porcentaje = (cantidad / total * 100) if total > 0 else 0
            datos_inventario.append({
                "Categoría": cat,
                "Cantidad": f"{cantidad:,}",
                "Porcentaje": f"{porcentaje:.1f}%"
            })
    
    if datos_inventario:
        st.dataframe(pd.DataFrame(datos_inventario), use_container_width=True)
    else:
        st.info("No hay inventario registrado aún")

# ============================================
# MÓDULO: CATEGORÍAS
# ============================================
elif menu == "🏷️ Categorías":
    st.title("🏷️ Gestión de Categorías de Huevos")
    
    st.write("### Categorías actuales")
    for cat in categorias_data["categorias"]:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"- **{cat}**")
        with col2:
            if cat not in ["Extra", "AAA", "AA", "A", "B"]:
                if st.button(f"🗑️ Eliminar {cat}", key=f"del_{cat}"):
                    if eliminar_categoria(cat):
                        st.success(f"✅ Categoría '{cat}' eliminada")
                        st.rerun()
                    else:
                        st.warning(f"⚠️ No se puede eliminar: tiene stock o es estándar")
    
    st.write("---")
    st.write("### Agregar nueva categoría")
    nueva_cat = st.text_input("Nombre de la nueva categoría (ej: Jumbo, C, Sucio)")
    if st.button("➕ Agregar categoría"):
        if agregar_categoria(nueva_cat.upper()):
            st.success(f"✅ Categoría '{nueva_cat.upper()}' agregada")
            st.rerun()
        else:
            st.error("❌ La categoría ya existe o está vacía")
    
    st.info("💡 **Nota:** Las categorías Extra, AAA, AA, A, B son estándar y no se pueden eliminar")

# ============================================
# MÓDULO: REPORTES
# ============================================
elif menu == "📊 Reportes":
    st.title("📊 Reportes de Producción")
    
    if produccion:
        df = pd.DataFrame(produccion)
        df["fecha"] = pd.to_datetime(df["fecha"])
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Desde", df["fecha"].min().date())
        with col2:
            fecha_fin = st.date_input("Hasta", df["fecha"].max().date())
        
        mask = (df["fecha"].dt.date >= fecha_inicio) & (df["fecha"].dt.date <= fecha_fin)
        df_filtrado = df[mask]
        
        if not df_filtrado.empty:
            total_periodo = df_filtrado["total_huevos"].sum()
            st.metric("Total producido en el período", f"{total_periodo:,} huevos")
            
            st.write("---")
            st.subheader("Producción por galpón")
            por_galpon = df_filtrado.groupby("galpon_id")["total_huevos"].sum().reset_index()
            for _, row in por_galpon.iterrows():
                galpon = next((g["nombre"] for g in galpones if g["id"] == row["galpon_id"]), "?")
                st.write(f"**{galpon}**: {row['total_huevos']:,} huevos")
            
            st.write("---")
            st.subheader("Detalle de registros")
            df_mostrar = df_filtrado[["fecha", "galpon_id", "total_huevos"]].copy()
            df_mostrar["galpon"] = df_mostrar["galpon_id"].apply(
                lambda x: next((g["nombre"] for g in galpones if g["id"] == x), "?")
            )
            df_mostrar = df_mostrar.rename(columns={"fecha": "Fecha", "total_huevos": "Total Huevos"})
            st.dataframe(df_mostrar[["Fecha", "galpon", "Total Huevos"]], use_container_width=True)
        else:
            st.info("No hay datos en el período seleccionado")
    else:
        st.info("No hay registros de producción aún")

# ============================================
# MÓDULO: USUARIOS
# ============================================
elif menu == "👥 Usuarios":
    st.title("👥 Gestión de Usuarios")
    
    st.write("### Usuarios actuales")
    for user, info in usuarios.items():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**{user}** - {info['nombre']} ({info['rol']})")
        with col2:
            if user != "admin":
                if st.button(f"🗑️ Eliminar {user}", key=f"del_user_{user}"):
                    del usuarios[user]
                    guardar_datos(USUARIOS_FILE, usuarios)
                    st.success(f"✅ Usuario '{user}' eliminado")
                    st.rerun()
    
    st.write("---")
    st.write("### Agregar nuevo usuario")
    with st.form("nuevo_usuario"):
        nuevo_user = st.text_input("Usuario")
        nuevo_nombre = st.text_input("Nombre completo")
        nuevo_pass = st.text_input("Contraseña", type="password")
        nuevo_rol = st.selectbox("Rol", ["produccion", "contador", "vendedor", "admin"])
        
        if st.form_submit_button("➕ Crear usuario"):
            if nuevo_user and nuevo_nombre and nuevo_pass:
                if nuevo_user not in usuarios:
                    usuarios[nuevo_user] = {
                        "password": hash_password(nuevo_pass),
                        "nombre": nuevo_nombre,
                        "rol": nuevo_rol
                    }
                    guardar_datos(USUARIOS_FILE, usuarios)
                    st.success(f"✅ Usuario '{nuevo_user}' creado")
                    st.rerun()
                else:
                    st.error("❌ El usuario ya existe")
            else:
                st.error("❌ Complete todos los campos")

# ============================================
# MÓDULO: CONFIGURACIÓN
# ============================================
elif menu == "⚙️ Configuración":
    st.title("⚙️ Configuración de Galpones")
    
    st.write("### Galpones registrados")
    for i, galpon in enumerate(galpones):
        with st.expander(f"📌 {galpon['nombre']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                nuevo_nombre = st.text_input("Nombre", value=galpon['nombre'], key=f"nombre_{i}")
            with col2:
                nueva_cantidad = st.number_input("Cantidad de gallinas", value=galpon['cantidad_gallinas'], key=f"cantidad_{i}")
            with col3:
                nuevo_estado = st.selectbox("Estado", ["produccion", "mantenimiento", "descanso", "descarte"], 
                                           index=["produccion", "mantenimiento", "descanso", "descarte"].index(galpon['estado']),
                                           key=f"estado_{i}")
            
            if st.button(f"💾 Guardar cambios", key=f"guardar_{i}"):
                galpones[i]["nombre"] = nuevo_nombre
                galpones[i]["cantidad_gallinas"] = nueva_cantidad
                galpones[i]["estado"] = nuevo_estado
                guardar_datos(GALPONES_FILE, galpones)
                st.success(f"✅ Galpón actualizado")
                st.rerun()
    
    st.write("---")
    st.write("### Agregar nuevo galpón")
    with st.form("nuevo_galpon"):
        nombre_galpon = st.text_input("Nombre del galpón")
        gallinas_galpon = st.number_input("Cantidad de gallinas", min_value=0, value=0)
        estado_galpon = st.selectbox("Estado", ["produccion", "mantenimiento", "descanso", "descarte"])
        
        if st.form_submit_button("➕ Agregar galpón"):
            if nombre_galpon:
                nuevo_id = max([g["id"] for g in galpones]) + 1 if galpones else 1
                galpones.append({
                    "id": nuevo_id,
                    "nombre": nombre_galpon,
                    "cantidad_gallinas": gallinas_galpon,
                    "estado": estado_galpon
                })
                guardar_datos(GALPONES_FILE, galpones)
                # Sincronizar inventario de gallinas
                inventario_gallinas[str(nuevo_id)] = {
                    "nombre": nombre_galpon,
                    "cantidad": gallinas_galpon,
                    "estado": estado_galpon
                }
                guardar_datos(INVENTARIO_GALLINAS_FILE, inventario_gallinas)
                st.success(f"✅ Galpón '{nombre_galpon}' agregado")
                st.rerun()
            else:
                st.error("❌ El nombre es obligatorio")
