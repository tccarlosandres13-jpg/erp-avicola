# ============================================
# MÓDULO: VENTAS
# ============================================

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modulos.datos import (
    galpones, inventario_huevos, produccion, guardar_datos, cargar_datos,
    INVENTARIO_HUEVOS_FILE, CATEGORIAS_FILE
)

# Archivo para ventas
VENTAS_FILE = 'ventas.json'

def cargar_ventas():
    return cargar_datos(VENTAS_FILE, [])

def guardar_ventas(ventas):
    guardar_datos(VENTAS_FILE, ventas)

def obtener_cliente_por_id(cliente_id, clientes):
    for c in clientes:
        if c.get("id") == cliente_id:
            return c
    return None

def mostrar_ventas():
    
    # Inicializar estados de navegación
    if 'seccion_ventas' not in st.session_state:
        st.session_state.seccion_ventas = "dashboard"
    
    # Cargar datos
    ventas = cargar_ventas()
    clientes = cargar_datos('clientes.json', [])
    categorias = cargar_datos(CATEGORIAS_FILE, {"categorias": ["Extra", "AAA", "AA", "A", "B"]})
    
    # ========== DASHBOARD DE VENTAS ==========
    if st.session_state.seccion_ventas == "dashboard":
        st.title("💰 Módulo de Ventas")
        
        # Botones de acción
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            if st.button("📝 Nueva Venta", key="btn_nueva_venta", use_container_width=True):
                st.session_state.seccion_ventas = "nueva_venta"
                st.rerun()
        with col_b2:
            if st.button("👥 Clientes", key="btn_clientes", use_container_width=True):
                st.session_state.seccion_ventas = "clientes"
                st.rerun()
        with col_b3:
            if st.button("📊 Historial de Ventas", key="btn_historial_ventas", use_container_width=True):
                st.session_state.seccion_ventas = "historial"
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Resumen de Ventas")
        
        # Calcular estadísticas
        hoy = datetime.now().strftime("%Y-%m-%d")
        ventas_hoy = [v for v in ventas if v.get("fecha", "") == hoy]
        total_hoy = sum(v.get("total", 0) for v in ventas_hoy)
        total_ventas = sum(v.get("total", 0) for v in ventas)
        
        # Crear tarjetas de resumen
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-number">{len(ventas_hoy)}</div>
                <div class="summary-label">📋 Ventas Hoy</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-number">${total_hoy:,.0f}</div>
                <div class="summary-label">💰 Total Hoy</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-number">{len(ventas)}</div>
                <div class="summary-label">📋 Total Ventas</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-number">${total_ventas:,.0f}</div>
                <div class="summary-label">💰 Total Facturado</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Últimas ventas
        st.write("---")
        st.subheader("📋 Últimas Ventas")
        
        if ventas:
            ultimas_ventas = ventas[-5:][::-1]
            for v in ultimas_ventas:
                cliente = obtener_cliente_por_id(v.get("cliente_id"), clientes)
                nombre_cliente = cliente.get("nombre", "Cliente no encontrado") if cliente else "Cliente no encontrado"
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{v.get('fecha', '')}** - {nombre_cliente}")
                    st.write(f"📦 {v.get('total_huevos', 0):,} huevos")
                with col2:
                    st.write(f"**${v.get('total', 0):,.0f}**")
                st.write("---")
        else:
            st.info("No hay ventas registradas aún.")
        
        st.info("👈 Presiona un botón para comenzar")
    
    # ========== NUEVA VENTA ==========
    elif st.session_state.seccion_ventas == "nueva_venta":
        st.title("📝 Nueva Venta")
        
        # Botón regresar
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_nueva_venta", use_container_width=True):
                st.session_state.seccion_ventas = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
        # Datos de inventario disponible
        total_inventario = inventario_huevos.get("Bodega1_total", 0)
        st.info(f"📦 **Inventario disponible:** {total_inventario:,} huevos")
        
        # Seleccionar cliente (o crear nuevo)
        col1, col2 = st.columns(2)
        
        with col1:
            # Lista de clientes
            clientes_list = [c.get("nombre", "Cliente sin nombre") for c in clientes]
            opciones_clientes = ["Nuevo Cliente"] + clientes_list
            cliente_seleccionado = st.selectbox("👤 Cliente", opciones_clientes, key="cliente_venta")
            
            if cliente_seleccionado == "Nuevo Cliente":
                nuevo_cliente_nombre = st.text_input("Nombre del cliente")
                nuevo_cliente_telefono = st.text_input("Teléfono")
                nuevo_cliente_direccion = st.text_input("Dirección")
            else:
                # Buscar cliente seleccionado
                cliente_info = None
                for c in clientes:
                    if c.get("nombre") == cliente_seleccionado:
                        cliente_info = c
                        break
                if cliente_info:
                    st.write(f"📞 {cliente_info.get('telefono', 'No tiene teléfono')}")
                    st.write(f"📍 {cliente_info.get('direccion', 'No tiene dirección')}")
        
        with col2:
            st.subheader("📦 Detalle de la venta")
            
            # Seleccionar categorías y cantidades
            clasificacion_venta = {}
            for cat in categorias.get("categorias", []):
                clasificacion_venta[cat] = st.number_input(
                    f"{cat}",
                    min_value=0,
                    value=0,
                    step=100,
                    key=f"venta_{cat}"
                )
            
            total_huevos_venta = sum(clasificacion_venta.values())
            
            # Precio por huevo (puedes ajustarlo)
            precio_unitario = st.number_input(
                "💰 Precio por unidad ($)",
                min_value=0,
                value=200,
                step=50,
                key="precio_unitario"
            )
            
            total_venta = total_huevos_venta * precio_unitario
            
            st.write("---")
            st.write(f"**📊 Total huevos:** {total_huevos_venta:,}")
            st.write(f"**💰 Total venta:** ${total_venta:,.0f}")
        
        # Botón guardar
        st.write("---")
        if st.button("✅ GUARDAR VENTA", type="primary", use_container_width=True):
            # Validar inventario
            if total_huevos_venta > total_inventario:
                st.error(f"❌ No hay suficiente inventario. Disponible: {total_inventario:,} huevos")
            elif total_huevos_venta == 0:
                st.error("❌ Debe seleccionar al menos un huevo")
            elif cliente_seleccionado == "Nuevo Cliente" and not nuevo_cliente_nombre:
                st.error("❌ Debe ingresar el nombre del nuevo cliente")
            else:
                # Crear o buscar cliente
                cliente_id = None
                if cliente_seleccionado == "Nuevo Cliente":
                    nuevo_cliente = {
                        "id": len(clientes) + 1,
                        "nombre": nuevo_cliente_nombre,
                        "telefono": nuevo_cliente_telefono,
                        "direccion": nuevo_cliente_direccion,
                        "fecha_registro": datetime.now().strftime("%Y-%m-%d")
                    }
                    clientes.append(nuevo_cliente)
                    guardar_datos('clientes.json', clientes)
                    cliente_id = nuevo_cliente["id"]
                else:
                    for c in clientes:
                        if c.get("nombre") == cliente_seleccionado:
                            cliente_id = c.get("id")
                            break
                
                # Registrar venta
                nueva_venta = {
                    "id": len(ventas) + 1,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "cliente_id": cliente_id,
                    "cliente_nombre": cliente_seleccionado if cliente_seleccionado != "Nuevo Cliente" else nuevo_cliente_nombre,
                    "clasificacion": clasificacion_venta,
                    "total_huevos": total_huevos_venta,
                    "precio_unitario": precio_unitario,
                    "total": total_venta
                }
                
                ventas.append(nueva_venta)
                guardar_ventas(ventas)
                
                # Descontar del inventario
                for cat, cantidad in clasificacion_venta.items():
                    if cantidad > 0:
                        inventario_huevos[f"Bodega1_{cat}"] = inventario_huevos.get(f"Bodega1_{cat}", 0) - cantidad
                        inventario_huevos["Bodega1_total"] = inventario_huevos.get("Bodega1_total", 0) - cantidad
                guardar_datos(INVENTARIO_HUEVOS_FILE, inventario_huevos)
                
                st.success(f"✅ Venta registrada: {total_huevos_venta:,} huevos por ${total_venta:,.0f}")
                st.balloons()
                st.session_state.seccion_ventas = "dashboard"
                st.rerun()
    
    # ========== CLIENTES ==========
    elif st.session_state.seccion_ventas == "clientes":
        st.title("👥 Gestión de Clientes")
        
        # Botón regresar
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_clientes", use_container_width=True):
                st.session_state.seccion_ventas = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
        # Lista de clientes
        st.subheader("📋 Lista de Clientes")
        if clientes:
            df_clientes = pd.DataFrame(clientes)
            st.dataframe(df_clientes, use_container_width=True, hide_index=True)
        else:
            st.info("No hay clientes registrados aún.")
        
        st.write("---")
        st.subheader("➕ Agregar Nuevo Cliente")
        
        col1, col2 = st.columns(2)
        with col1:
            nuevo_cliente_nombre = st.text_input("Nombre completo", key="new_cliente_nombre")
            nuevo_cliente_telefono = st.text_input("Teléfono", key="new_cliente_telefono")
        with col2:
            nuevo_cliente_direccion = st.text_input("Dirección", key="new_cliente_direccion")
            nuevo_cliente_email = st.text_input("Email", key="new_cliente_email")
        
        if st.button("➕ Agregar Cliente", type="primary"):
            if nuevo_cliente_nombre:
                nuevo_cliente = {
                    "id": len(clientes) + 1,
                    "nombre": nuevo_cliente_nombre,
                    "telefono": nuevo_cliente_telefono,
                    "direccion": nuevo_cliente_direccion,
                    "email": nuevo_cliente_email,
                    "fecha_registro": datetime.now().strftime("%Y-%m-%d")
                }
                clientes.append(nuevo_cliente)
                guardar_datos('clientes.json', clientes)
                st.success(f"✅ Cliente '{nuevo_cliente_nombre}' agregado correctamente")
                st.rerun()
            else:
                st.error("❌ El nombre del cliente es obligatorio")
    
    # ========== HISTORIAL DE VENTAS ==========
    elif st.session_state.seccion_ventas == "historial":
        st.title("📊 Historial de Ventas")
        
        # Botón regresar
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_historial_ventas", use_container_width=True):
                st.session_state.seccion_ventas = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
        if ventas:
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                fecha_desde = st.date_input("Desde", datetime.now() - timedelta(days=30), key="ventas_desde")
            with col2:
                fecha_hasta = st.date_input("Hasta", datetime.now(), key="ventas_hasta")
            
            fecha_desde_str = fecha_desde.strftime("%Y-%m-%d")
            fecha_hasta_str = fecha_hasta.strftime("%Y-%m-%d")
            
            # Filtrar ventas
            ventas_filtradas = []
            for v in ventas:
                fecha_venta = v.get("fecha", "").split(" ")[0]  # Tomar solo la fecha (YYYY-MM-DD)
                if fecha_desde_str <= fecha_venta <= fecha_hasta_str:
                    ventas_filtradas.append(v)
            
            if ventas_filtradas:
                # Convertir a DataFrame
                df_ventas = pd.DataFrame(ventas_filtradas)
                
                # Mostrar resumen
                total_periodo = df_ventas["total"].sum()
                total_huevos_periodo = df_ventas["total_huevos"].sum()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📋 Ventas", f"{len(ventas_filtradas)}")
                with col2:
                    st.metric("🥚 Huevos vendidos", f"{total_huevos_periodo:,}")
                with col3:
                    st.metric("💰 Total facturado", f"${total_periodo:,.0f}")
                
                st.write("---")
                st.subheader("📋 Detalle de ventas")
                
                # Mostrar tabla
                df_mostrar = df_ventas[["fecha", "cliente_nombre", "total_huevos", "total"]]
                df_mostrar = df_mostrar.rename(columns={
                    "fecha": "Fecha",
                    "cliente_nombre": "Cliente",
                    "total_huevos": "Huevos",
                    "total": "Total"
                })
                st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
            else:
                st.info("No hay ventas en el período seleccionado")
        else:
            st.info("No hay ventas registradas aún.")
