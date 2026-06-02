# ============================================
# ERP AVICOLA - PRODUCCIÓN DE HUEVOS
# Versión 1.0 - Con Login y Módulo de Producción
# ============================================

import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import json
import os

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

# Archivos para guardar datos
USUARIOS_FILE = 'usuarios.json'
GALPONES_FILE = 'galpones.json'
PRODUCCION_FILE = 'produccion.json'
INVENTARIO_FILE = 'inventario.json'
CATEGORIAS_FILE = 'categorias.json'

# ============================================
# FUNCIONES PARA CARGAR/GUARDAR DATOS
# ============================================

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

# ============================================
# DATOS POR DEFECTO
# ============================================

# Usuarios: admin / admin123
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

# Galpones por defecto
GALPONES_POR_DEFECTO = [
    {"id": 1, "nombre": "Galpón 1", "cantidad_gallinas": 75000, "estado": "produccion"},
    {"id": 2, "nombre": "Galpón 2", "cantidad_gallinas": 0, "estado": "mantenimiento"},
    {"id": 3, "nombre": "Galpón 3", "cantidad_gallinas": 25000, "estado": "produccion"},
    {"id": 4, "nombre": "Galpón Levante", "cantidad_gallinas": 0, "estado": "descanso"}
]

# Categorías de huevos por defecto
CATEGORIAS_POR_DEFECTO = {
    "categorias": ["Extra", "AAA", "AA", "A", "B"],
    "editable": True
}

# ============================================
# INICIALIZAR DATOS
# ============================================

usuarios = cargar_datos(USUARIOS_FILE, USUARIOS_POR_DEFECTO)
galpones = cargar_datos(GALPONES_FILE, GALPONES_POR_DEFECTO)
produccion = cargar_datos(PRODUCCION_FILE, [])
inventario = cargar_datos(INVENTARIO_FILE, {})
categorias_data = cargar_datos(CATEGORIAS_FILE, CATEGORIAS_POR_DEFECTO)

if not inventario:
    for cat in categorias_data["categorias"]:
        inventario[f"Bodega1_{cat}"] = 0
    inventario["Bodega1_total"] = 0

# ============================================
# FUNCIONES DEL NEGOCIO
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
        inventario[f"Bodega1_{categoria}"] = inventario.get(f"Bodega1_{categoria}", 0) + cantidad
        inventario["Bodega1_total"] = inventario.get("Bodega1_total", 0) + cantidad
    guardar_datos(INVENTARIO_FILE, inventario)
    return nuevo_registro

def agregar_categoria(nueva_categoria):
    if nueva_categoria and nueva_categoria not in categorias_data["categorias"]:
        categorias_data["categorias"].append(nueva_categoria)
        guardar_datos(CATEGORIAS_FILE, categorias_data)
        inventario[f"Bodega1_{nueva_categoria}"] = 0
        guardar_datos(INVENTARIO_FILE, inventario)
        return True
    return False

def eliminar_categoria(categoria):
    if categoria in categorias_data["categorias"] and categoria not in ["Extra", "AAA", "AA", "A", "B"]:
        if inventario.get(f"Bodega1_{categoria}", 0) == 0:
            categorias_data["categorias"].remove(categoria)
            guardar_datos(CATEGORIAS_FILE, categorias_data)
            return True
    return False

# ============================================
# INTERFAZ DE LOGIN
# ============================================

st.set_page_config(page_title="ERP Avícola", page_icon="🐔", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

if not st.session_state.logged_in:
    st.title("🐔 ERP Avícola - Inicio de Sesión")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar", type="primary"):
            if usuario in usuarios and usuarios[usuario]["password"] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.usuario = usuario
                st.session_state.rol = usuarios[usuario]["rol"]
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
    
    with col2:
        st.info("📝 **Credenciales de prueba:**\n\n- Usuario: `admin`\n- Contraseña: `admin123`\n\n- Usuario: `auxiliar`\n- Contraseña: `produccion123`")
    
    st.stop()

# ============================================
# MENÚ PRINCIPAL
# ============================================

usuario_actual = st.session_state.usuario
rol_actual = st.session_state.rol

st.sidebar.title(f"🐔 ERP Avícola")
st.sidebar.write(f"**Usuario:** {usuario_actual}")
st.sidebar.write(f"**Rol:** {rol_actual}")
st.sidebar.write("---")

if rol_actual == "admin":
    menu = st.sidebar.radio("📋 Menú Principal", [
        "🏠 Dashboard",
        "🐔 Producción",
        "📦 Inventario",
        "🏷️ Categorías",
        "📊 Reportes",
        "👥 Usuarios",
        "⚙️ Configuración"
    ])
else:
    menu = st.sidebar.radio("📋 Menú Principal", [
        "🏠 Dashboard",
        "🐔 Producción",
        "📦 Inventario",
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
    
    col1, col2, col3 = st.columns(3)
    
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    
    total_inventario = inventario.get("Bodega1_total", 0)
    galpones_activos = [g for g in galpones if g["estado"] == "produccion"]
    total_gallinas = sum(g["cantidad_gallinas"] for g in galpones_activos)
    
    col1.metric("🥚 Producción Hoy", f"{total_hoy:,} huevos")
    col2.metric("📦 Inventario Bodega 1", f"{total_inventario:,} huevos")
    col3.metric("🐔 Gallinas en Producción", f"{total_gallinas:,}")
    
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
# MÓDULO: PRODUCCIÓN
# ============================================
elif menu == "🐔 Producción":
    st.title("🐔 Registro de Producción Diaria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        galpones_activos = [g for g in galpones if g["estado"] == "produccion"]
        if not galpones_activos:
            st.warning("⚠️ No hay galpones activos. Revisa la configuración.")
        else:
            galpon_seleccionado = st.selectbox(
                "Seleccione el galpón",
                galpones_activos,
                format_func=lambda x: f"{x['nombre']} ({x['cantidad_gallinas']:,} gallinas)"
            )
            
            fecha = st.date_input("Fecha de producción", datetime.now())
            
            st.write("---")
            st.subheader("Clasificación de huevos")
            
            clasificacion = {}
            cols = st.columns(2)
            for i, cat in enumerate(categorias_data["categorias"]):
                with cols[i % 2]:
                    clasificacion[cat] = st.number_input(f"{cat}", min_value=0, value=0, step=100)
            
            total_ingresado = sum(clasificacion.values())
            st.info(f"📊 Total de huevos a registrar: {total_ingresado:,}")
            
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

# ============================================
# MÓDULO: INVENTARIO
# ============================================
elif menu == "📦 Inventario":
    st.title("📦 Inventario - Bodega 1 (Granja San Miguel)")
    
    total = inventario.get("Bodega1_total", 0)
    st.metric("Total de huevos en bodega", f"{total:,}")
    
    st.write("---")
    st.subheader("📊 Detalle por categoría")
    
    datos_inventario = []
    for cat in categorias_data["categorias"]:
        cantidad = inventario.get(f"Bodega1_{cat}", 0)
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
                st.success(f"✅ Galpón '{nombre_galpon}' agregado")
                st.rerun()
            else:
                st.error("❌ El nombre es obligatorio")
