# ============================================
# ERP AVICOLA - HUEVOS DOÑA DORA
# Versión FINAL - Con contador y botón regresar independiente
# ============================================

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import json
import os
from PIL import Image

st.set_page_config(page_title="Doña Dora - ERP", page_icon="🥚", layout="wide")

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
    
    /* Botón regresar */
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
    
    /* Contador en línea */
    .contador-linea {
        display: inline-block;
        background-color: #2E7D32;
        color: white;
        border-radius: 20px;
        padding: 5px 15px;
        font-weight: bold;
        margin-left: 15px;
        font-size: 14px;
    }
    
    .titulo-con-contador {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def cargar_logo():
    logo_path = "logo.jpeg"
    if os.path.exists(logo_path):
        return Image.open(logo_path)
    else:
        logo_path_jpg = "logo.jpg"
        if os.path.exists(logo_path_jpg):
            return Image.open(logo_path_jpg)
    return None

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

USUARIOS_POR_DEFECTO = {
    "admin": {"password": hash_password("admin123"), "nombre": "Administrador", "rol": "admin"},
    "auxiliar": {"password": hash_password("produccion123"), "nombre": "Auxiliar de Producción", "rol": "produccion"}
}

GALPONES_POR_DEFECTO = [
    {"id": 1, "nombre": "Galpón 1", "cantidad_gallinas": 75000, "estado": "produccion"},
    {"id": 2, "nombre": "Galpón 2", "cantidad_gallinas": 0, "estado": "mantenimiento"},
    {"id": 3, "nombre": "Galpón 3", "cantidad_gallinas": 25000, "estado": "produccion"},
    {"id": 4, "nombre": "Galpón Levante", "cantidad_gallinas": 0, "estado": "descanso"}
]

CATEGORIAS_POR_DEFECTO = {"categorias": ["Extra", "AAA", "AA", "A", "B"], "editable": True}

usuarios = cargar_datos(USUARIOS_FILE, USUARIOS_POR_DEFECTO)
galpones = cargar_datos(GALPONES_FILE, GALPONES_POR_DEFECTO)
produccion = cargar_datos(PRODUCCION_FILE, [])
inventario_huevos = cargar_datos(INVENTARIO_HUEVOS_FILE, {})
categorias_data = cargar_datos(CATEGORIAS_FILE, CATEGORIAS_POR_DEFECTO)
inventario_gallinas = cargar_datos(INVENTARIO_GALLINAS_FILE, {})
movimientos_gallinas = cargar_datos(MOVIMIENTOS_GALLINAS_FILE, [])

if not inventario_gallinas:
    for g in galpones:
        inventario_gallinas[str(g["id"])] = {"nombre": g["nombre"], "cantidad": g["cantidad_gallinas"], "estado": g["estado"]}
    guardar_datos(INVENTARIO_GALLINAS_FILE, inventario_gallinas)

if not inventario_huevos:
    for cat in categorias_data["categorias"]:
        inventario_huevos[f"Bodega1_{cat}"] = 0
    inventario_huevos["Bodega1_total"] = 0
    guardar_datos(INVENTARIO_HUEVOS_FILE, inventario_huevos)

def registrar_movimiento_gallinas(galpon_id, tipo_movimiento, cantidad, motivo, fecha):
    galpon = next((g for g in galpones if g["id"] == galpon_id), None)
    if not galpon:
        return False, "Galpón no encontrado"
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
    movimiento = {"id": len(movimientos_gallinas) + 1, "galpon_id": galpon_id, "galpon_nombre": galpon["nombre"], "fecha": fecha, "tipo": tipo_movimiento, "cantidad": cantidad, "motivo": motivo, "cantidad_anterior": cantidad_actual, "cantidad_nueva": nueva_cantidad}
    movimientos_gallinas.append(movimiento)
    guardar_datos(MOVIMIENTOS_GALLINAS_FILE, movimientos_gallinas)
    inventario_gallinas[str(galpon_id)] = {"nombre": galpon["nombre"], "cantidad": nueva_cantidad, "estado": galpon["estado"]}
    guardar_datos(INVENTARIO_GALLINAS_FILE, inventario_gallinas)
    for g in galpones:
        if g["id"] == galpon_id:
            g["cantidad_gallinas"] = nueva_cantidad
            break
    guardar_datos(GALPONES_FILE, galpones)
    return True, movimiento

def obtener_postura_real_periodo(galpon_id, fecha_inicio, fecha_fin):
    producciones_galpon = [p for p in produccion if p["galpon_id"] == galpon_id and fecha_inicio <= p["fecha"] <= fecha_fin]
    if not producciones_galpon:
        return 0
    total_huevos = sum(p["total_huevos"] for p in producciones_galpon)
    promedio_diario = total_huevos / len(producciones_galpon)
    cantidad_gallinas = inventario_gallinas.get(str(galpon_id), {}).get("cantidad", 0)
    if cantidad_gallinas == 0:
        return 0
    return round((promedio_diario / cantidad_gallinas) * 100, 1)

def obtener_mortalidad_periodo(galpon_id, fecha_inicio, fecha_fin):
    return sum(m["cantidad"] for m in movimientos_gallinas if m["galpon_id"] == galpon_id and m["tipo"] == "mortalidad" and fecha_inicio <= m["fecha"] <= fecha_fin)

def registrar_produccion(galpon_id, fecha, clasificacion):
    nuevo_registro = {"id": len(produccion) + 1, "galpon_id": galpon_id, "fecha": fecha, "clasificacion": clasificacion, "total_huevos": sum(clasificacion.values())}
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

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        logo = cargar_logo()
        if logo:
            st.image(logo, width=150)
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
        "🏠 Dashboard", "🐔 Producción", "📦 Inventario Huevos",
        "🏷️ Categorías", "📊 Reportes", "👥 Usuarios", "⚙️ Configuración"
    ])
else:
    menu = st.sidebar.radio("📋 Menú Principal", [
        "🏠 Dashboard", "🐔 Producción", "📦 Inventario Huevos", "📊 Reportes"
    ])

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.logged_in = False
    st.session_state.usuario = None
    st.rerun()

if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard - Resumen del Día")
    col1, col2, col3, col4 = st.columns(4)
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    total_inventario = inventario_huevos.get("Bodega1_total", 0)
    total_gallinas = sum(g.get("cantidad", 0) for g in inventario_gallinas.values())
    mes_actual = datetime.now().strftime("%Y-%m")
    mortalidad_mes = sum(m["cantidad"] for m in movimientos_gallinas if m["tipo"] == "mortalidad" and m["fecha"].startswith(mes_actual))
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

elif menu == "🐔 Producción":
    
    if 'seccion_produccion' not in st.session_state:
        st.session_state.seccion_produccion = "dashboard"
    
    if st.session_state.seccion_produccion == "dashboard":
        st.title("🐔 Gestión de Producción")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            if st.button("📝 Registrar Producción", key="btn_registrar", use_container_width=True):
                st.session_state.seccion_produccion = "registrar"
                st.rerun()
        with col_b2:
            if st.button("🐔 Inventario Gallinas", key="btn_inventario", use_container_width=True):
                st.session_state.seccion_produccion = "inventario"
                st.rerun()
        with col_b3:
            if st.button("📜 Historial Gallinas", key="btn_historial", use_container_width=True):
                st.session_state.seccion_produccion = "historial"
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Resumen de Inventario de Gallinas")
        
        fecha_fin_default = datetime.now()
        fecha_inicio_default = fecha_fin_default - timedelta(days=30)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("📅 **Desde**")
            fecha_inicio = st.date_input("", value=fecha_inicio_default, key="fecha_inicio_input", label_visibility="collapsed")
        with col_f2:
            st.markdown("📅 **Hasta**")
            fecha_fin = st.date_input("", value=fecha_fin_default, key="fecha_fin_input", label_visibility="collapsed")
        
        fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%d")
        fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")
        
        st.caption(f"📌 Mostrando datos desde el **{fecha_inicio_str}** hasta el **{fecha_fin_str}**")
        st.markdown("---")
        
        produccion = cargar_datos(PRODUCCION_FILE, [])
        movimientos_gallinas = cargar_datos(MOVIMIENTOS_GALLINAS_FILE, [])
        
        datos_resumen = []
        total_gallinas_generales = 0
        total_produccion_esperada = 0
        
        for galpon in galpones:
            galpon_id = galpon["id"]
            cantidad = inventario_gallinas.get(str(galpon_id), {}).get("cantidad", 0)
            total_gallinas_generales += cantidad
            produccion_esperada = int(cantidad * 0.9)
            total_produccion_esperada += produccion_esperada
            mortalidad_periodo = obtener_mortalidad_periodo(galpon_id, fecha_inicio_str, fecha_fin_str)
            postura_real = obtener_postura_real_periodo(galpon_id, fecha_inicio_str, fecha_fin_str)
            estado_color = {"produccion": "🟢", "mantenimiento": "🟡", "descanso": "🔵", "descarte": "🔴"}.get(galpon["estado"], "⚪")
            if postura_real >= 85:
                indicador = "🟢 Normal"
            elif postura_real >= 70:
                indicador = "🟡 Atención"
            else:
                indicador = "🔴 Crítico"
            datos_resumen.append({
                "Estado": f"{estado_color} {galpon['estado'].capitalize()}",
                "Galpón": galpon["nombre"],
                "Gallinas actuales": f"{cantidad:,}",
                "Prod. esperada (90%)": f"{produccion_esperada:,}",
                "Mortalidad (periodo)": f"{mortalidad_periodo:,}",
                "Postura real": f"{postura_real}%",
                "Indicador": indicador
            })
        
        df_resumen = pd.DataFrame(datos_resumen)
        st.dataframe(df_resumen, use_container_width=True, hide_index=True)
        
        total_mortalidad_periodo = sum(obtener_mortalidad_periodo(g["id"], fecha_inicio_str, fecha_fin_str) for g in galpones)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="summary-card"><div class="summary-number">{total_gallinas_generales:,}</div><div class="summary-label">🐔 TOTAL GALLINAS EN PRODUCCIÓN</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="summary-card"><div class="summary-number">{total_produccion_esperada:,}</div><div class="summary-label">🥚 PRODUCCIÓN ESPERADA (90%)</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="summary-card"><div class="summary-number">{total_mortalidad_periodo:,}</div><div class="summary-label">⚠️ MORTALIDAD EN EL PERIODO</div></div>', unsafe_allow_html=True)
        
        st.info("👈 Presiona un botón para realizar una acción específica")
    
    # ========== SECCIÓN: REGISTRAR PRODUCCIÓN ==========
    elif st.session_state.seccion_produccion == "registrar":
        st.title("📝 Registrar Producción Diaria")
        
        # Botón regresar (flecha)
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_registrar", use_container_width=True):
                st.session_state.seccion_produccion = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            galpones_activos = [g for g in galpones if g["estado"] == "produccion" and g["cantidad_gallinas"] > 0]
            if not galpones_activos:
                st.warning("⚠️ No hay galpones activos con gallinas.")
            else:
                galpon_seleccionado = st.selectbox(
                    "Seleccione el galpón",
                    galpones_activos,
                    format_func=lambda x: f"{x['nombre']} ({x['cantidad_gallinas']:,} gallinas)",
                    key="prod_galpon"
                )
                
                fecha = st.date_input("Fecha de producción", datetime.now())
                
                st.write("---")
                
                # Título con contador dinámico
                st.markdown("### Clasificación de huevos")
                
                # Crear campos de entrada
                clasificacion = {}
                cols = st.columns(2)
                for i, cat in enumerate(categorias_data["categorias"]):
                    with cols[i % 2]:
                        clasificacion[cat] = st.number_input(f"{cat}", min_value=0, value=0, step=100, key=f"cat_{cat}")
                
                # Calcular total en tiempo real
                total_ingresado = sum(clasificacion.values())
                
                # Mostrar contador junto al botón
                st.markdown(f"---")
                st.markdown(f"### 📊 TOTAL: **{total_ingresado:,}** huevos")
                
                if st.button("✅ GUARDAR Producción", type="primary", key="guardar_prod"):
                    if total_ingresado > 0:
                        clasificacion_filtrada = {k: v for k, v in clasificacion.items() if v > 0}
                        registrar_produccion(
                            galpon_seleccionado["id"],
                            fecha.strftime("%Y-%m-%d"),
                            clasificacion_filtrada
                        )
                        st.success(f"✅ Producción registrada: {total_ingresado:,} huevos")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Debe ingresar al menos un huevo")
        
        with col2:
            st.subheader("📋 Instrucciones")
            st.write("""
            1. Selecciona el **galpón** que terminó de recolectar
            2. Ingresa la **fecha** (hoy por defecto)
            3. Anota los números de la **clasificadora**
            4. Completa cada categoría
            5. Presiona **GUARDAR** para registrar la producción
            """)
            
            # Mostrar producción esperada
            if galpones_activos and 'galpon_seleccionado' in locals():
                gallinas_galpon = galpon_seleccionado["cantidad_gallinas"]
                produccion_esperada = int(gallinas_galpon * 0.9)
                st.info(f"📊 Producción esperada para este galpón (90%): **{produccion_esperada:,}** huevos")
    
    # ========== SECCIÓN: INVENTARIO GALLINAS ==========
    elif st.session_state.seccion_produccion == "inventario":
        st.title("🐔 Inventario de Gallinas")
        
        # Botón regresar (flecha)
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_inventario", use_container_width=True):
                st.session_state.seccion_produccion = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
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
                }.get(x, x),
                key="tipo_mov"
            )
        
        with col2:
            cantidad_mov = st.number_input("Cantidad de gallinas", min_value=1, value=1, step=10, key="cant_mov")
            
            motivos = {
                "levante": ["Llegada de pollitas", "Traslado desde levante", "Compra de aves"],
                "mortalidad": ["Enfermedad", "Golpe de calor", "Canibalismo", "Problema respiratorio", "Otra causa"],
                "descarte": ["Fin de ciclo", "Baja producción", "Enfermedad crónica", "Renovación de lote"]
            }
            
            motivo = st.selectbox("Motivo", motivos.get(tipo_movimiento, ["Otro"]), key="motivo")
            motivo_extra = st.text_input("Observaciones adicionales (opcional)", placeholder="Detalles específicos...", key="motivo_extra")
            motivo_completo = motivo + (f" - {motivo_extra}" if motivo_extra else "")
        
        fecha_mov = st.date_input("Fecha del movimiento", datetime.now(), key="fecha_mov")
        
        if st.button("✅ GUARDAR Movimiento", type="primary", key="guardar_mov"):
            cantidad_actual = inventario_gallinas.get(str(galpon_mov["id"]), {}).get("cantidad", 0)
            
            if tipo_movimiento == "mortalidad" and cantidad_mov > cantidad_actual:
                st.error(f"❌ No hay suficientes gallinas. Actualmente hay {cantidad_actual:,} gallinas.")
            elif tipo_movimiento == "descarte" and cantidad_mov > cantidad_actual:
                st.error(f"❌ No hay suficientes gallinas. Actualmente hay {cantidad_actual:,} gallinas.")
            else:
                success, _ = registrar_movimiento_gallinas(
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
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Error al registrar el movimiento")
    
    # ========== SECCIÓN: HISTORIAL GALLINAS ==========
    elif st.session_state.seccion_produccion == "historial":
        st.title("📜 Historial de Movimientos de Gallinas")
        
        # Botón regresar (flecha)
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_historial", use_container_width=True):
                st.session_state.seccion_produccion = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fecha_hist_desde = st.date_input("Desde", datetime.now() - timedelta(days=30), key="hist_desde")
        with col_f2:
            fecha_hist_hasta = st.date_input("Hasta", datetime.now(), key="hist_hasta")
        
        fecha_desde_str = fecha_hist_desde.strftime("%Y-%m-%d")
        fecha_hasta_str = fecha_hist_hasta.strftime("%Y-%m-%d")
        
        if movimientos_gallinas:
            movimientos_filtrados = [m for m in movimientos_gallinas if fecha_desde_str <= m["fecha"] <= fecha_hasta_str]
            
            if movimientos_filtrados:
                tipos = ["Todos"] + sorted(list(set(m["tipo"] for m in movimientos_filtrados)))
                filtro_tipo = st.selectbox("Filtrar por tipo", tipos)
                
                if filtro_tipo != "Todos":
                    movimientos_filtrados = [m for m in movimientos_filtrados if m["tipo"] == filtro_tipo]
                
                if movimientos_filtrados:
                    df_mov = pd.DataFrame(movimientos_filtrados[::-1])
                    df_mov["tipo_icono"] = df_mov["tipo"].map({"levante": "➕", "mortalidad": "⚠️", "descarte": "📤"})
                    df_mostrar = df_mov[["fecha", "tipo_icono", "galpon_nombre", "cantidad", "motivo", "cantidad_anterior", "cantidad_nueva"]]
                    df_mostrar.columns = ["Fecha", " ", "Galpón", "Cantidad", "Motivo", "Anterior", "Nueva"]
                    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
                    
                    st.write("---")
                    st.subheader("📊 Resumen de movimientos en el período")
                    col1, col2, col3 = st.columns(3)
                    total_levante = sum(m["cantidad"] for m in movimientos_filtrados if m["tipo"] == "levante")
                    total_mortalidad = sum(m["cantidad"] for m in movimientos_filtrados if m["tipo"] == "mortalidad")
                    total_descarte = sum(m["cantidad"] for m in movimientos_filtrados if m["tipo"] == "descarte")
                    col1.metric("➕ Total Levante", f"{total_levante:,}")
                    col2.metric("⚠️ Total Mortalidad", f"{total_mortalidad:,}")
                    col3.metric("📤 Total Descarte", f"{total_descarte:,}")
                else:
                    st.info("No hay movimientos con el filtro seleccionado.")
            else:
                st.info(f"No hay movimientos en el período seleccionado ({fecha_desde_str} a {fecha_hasta_str})")
        else:
            st.info("No hay movimientos registrados aún.")

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
            datos_inventario.append({"Categoría": cat, "Cantidad": f"{cantidad:,}", "Porcentaje": f"{porcentaje:.1f}%"})
    if datos_inventario:
        st.dataframe(pd.DataFrame(datos_inventario), use_container_width=True, hide_index=True)
    else:
        st.info("No hay inventario registrado aún")

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
            df_mostrar["galpon"] = df_mostrar["galpon_id"].apply(lambda x: next((g["nombre"] for g in galpones if g["id"] == x), "?"))
            df_mostrar = df_mostrar.rename(columns={"fecha": "Fecha", "total_huevos": "Total Huevos"})
            st.dataframe(df_mostrar[["Fecha", "galpon", "Total Huevos"]], use_container_width=True, hide_index=True)
        else:
            st.info("No hay datos en el período seleccionado")
    else:
        st.info("No hay registros de producción aún")

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
                    usuarios[nuevo_user] = {"password": hash_password(nuevo_pass), "nombre": nuevo_nombre, "rol": nuevo_rol}
                    guardar_datos(USUARIOS_FILE, usuarios)
                    st.success(f"✅ Usuario '{nuevo_user}' creado")
                    st.rerun()
                else:
                    st.error("❌ El usuario ya existe")
            else:
                st.error("❌ Complete todos los campos")

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
                nuevo_estado = st.selectbox("Estado", ["produccion", "mantenimiento", "descanso", "descarte"], index=["produccion", "mantenimiento", "descanso", "descarte"].index(galpon['estado']), key=f"estado_{i}")
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
                galpones.append({"id": nuevo_id, "nombre": nombre_galpon, "cantidad_gallinas": gallinas_galpon, "estado": estado_galpon})
                guardar_datos(GALPONES_FILE, galpones)
                inventario_gallinas[str(nuevo_id)] = {"nombre": nombre_galpon, "cantidad": gallinas_galpon, "estado": estado_galpon}
                guardar_datos(INVENTARIO_GALLINAS_FILE, inventario_gallinas)
                st.success(f"✅ Galpón '{nombre_galpon}' agregado")
                st.rerun()
            else:
                st.error("❌ El nombre es obligatorio")
