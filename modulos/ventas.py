# ============================================
# MÓDULO: VENTAS - PEDBOX AVÍCOLA
# Versión 1.0 - Con soporte para app móvil
# ============================================

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from modulos.datos import (
    galpones, inventario_huevos, produccion, 
    guardar_datos, cargar_datos,
    INVENTARIO_HUEVOS_FILE, CATEGORIAS_FILE
)

# ============================================
# ARCHIVOS DE DATOS
# ============================================

VENTAS_FILE = 'ventas.json'
CLIENTES_FILE = 'clientes.json'
PEDIDOS_FILE = 'pedidos.json'
PRODUCTOS_FILE = 'productos.json'

# ============================================
# FUNCIONES DE CARGA/GUARDADO
# ============================================

def cargar_ventas():
    return cargar_datos(VENTAS_FILE, [])

def guardar_ventas(ventas):
    guardar_datos(VENTAS_FILE, ventas)

def cargar_clientes():
    return cargar_datos(CLIENTES_FILE, [])

def guardar_clientes(clientes):
    guardar_datos(CLIENTES_FILE, clientes)

def cargar_pedidos():
    return cargar_datos(PEDIDOS_FILE, [])

def guardar_pedidos(pedidos):
    guardar_datos(PEDIDOS_FILE, pedidos)

# ============================================
# FUNCIÓN PARA OBTENER CLIENTE POR ID
# ============================================

def obtener_cliente_por_id(cliente_id, clientes):
    for c in clientes:
        if c.get("id") == cliente_id:
            return c
    return None

# ============================================
# FUNCIÓN PARA GENERAR NÚMERO DE FACTURA
# ============================================

def generar_numero_factura():
    ventas = cargar_ventas()
    if ventas:
        ultimo = ventas[-1]
        if "factura" in ultimo:
            try:
                num = int(ultimo["factura"].replace("FV-", "")) + 1
                return f"FV-{num:06d}"
            except:
                return "FV-000001"
    return "FV-000001"

# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def mostrar_ventas():
    
    if 'seccion_ventas' not in st.session_state:
        st.session_state.seccion_ventas = "dashboard"
    
    # Cargar datos
    ventas = cargar_ventas()
    clientes = cargar_clientes()
    pedidos = cargar_pedidos()
    categorias = cargar_datos(CATEGORIAS_FILE, {"categorias": ["Extra", "AAA", "AA", "A", "B"]})
    
    # ============================================
    # DASHBOARD DE VENTAS
    # ============================================
    if st.session_state.seccion_ventas == "dashboard":
        st.title("💰 Módulo de Ventas - PedBox")
        
        # Botones de acción
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            if st.button("📝 Nueva Venta", key="btn_nueva_venta", use_container_width=True):
                st.session_state.seccion_ventas = "nueva_venta"
                st.rerun()
        with col_b2:
            if st.button("👥 Clientes", key="btn_clientes", use_container_width=True):
                st.session_state.seccion_ventas = "clientes"
                st.rerun()
        with col_b3:
            if st.button("📋 Pedidos", key="btn_pedidos", use_container_width=True):
                st.session_state.seccion_ventas = "pedidos"
                st.rerun()
        with col_b4:
            if st.button("📊 Historial", key="btn_historial", use_container_width=True):
                st.session_state.seccion_ventas = "historial"
                st.rerun()
        
        st.markdown("---")
        
        # ========== TARJETAS DE RESULTADOS ==========
        hoy = datetime.now().strftime("%Y-%m-%d")
        ventas_hoy = [v for v in ventas if v.get("fecha", "").startswith(hoy)]
        total_hoy = sum(v.get("total", 0) for v in ventas_hoy)
        total_ventas = sum(v.get("total", 0) for v in ventas)
        
        # Ventas de la semana
        semana_inicio = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        ventas_semana = [v for v in ventas if v.get("fecha", "").startswith(semana_inicio)]
        total_semana = sum(v.get("total", 0) for v in ventas_semana)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border-radius:16px;padding:18px 20px;border:1px solid rgba(255,255,255,0.05);text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#FFD600;">{len(ventas_hoy)}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4);letter-spacing:1px;">VENTAS HOY</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border-radius:16px;padding:18px 20px;border:1px solid rgba(255,255,255,0.05);text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#FFD600;">${total_hoy:,.0f}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4);letter-spacing:1px;">TOTAL HOY</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border-radius:16px;padding:18px 20px;border:1px solid rgba(255,255,255,0.05);text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#FFD600;">${total_semana:,.0f}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4);letter-spacing:1px;">ÚLTIMA SEMANA</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border-radius:16px;padding:18px 20px;border:1px solid rgba(255,255,255,0.05);text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#FFD600;">${total_ventas:,.0f}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4);letter-spacing:1px;">TOTAL GENERAL</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ========== ÚLTIMAS VENTAS ==========
        st.subheader("📋 Últimas Ventas")
        
        if ventas:
            ultimas_ventas = ventas[-5:][::-1]
            for v in ultimas_ventas:
                cliente = obtener_cliente_por_id(v.get("cliente_id"), clientes)
                nombre_cliente = cliente.get("nombre", "Cliente no encontrado") if cliente else "Cliente no encontrado"
                
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{v.get('fecha', '').split(' ')[0]}** - {nombre_cliente}")
                    st.write(f"📦 {v.get('total_huevos', 0):,} huevos")
                with col2:
                    st.write(f"**Factura:** {v.get('factura', 'N/A')}")
                with col3:
                    st.write(f"**${v.get('total', 0):,.0f}**")
                st.markdown("---")
        else:
            st.info("No hay ventas registradas aún.")
        
        st.info("📱 **App Móvil:** Para usar desde el celular, descarga la app conectada a este sistema.")
    
    # ============================================
    # NUEVA VENTA
    # ============================================
    elif st.session_state.seccion_ventas == "nueva_venta":
        st.title("📝 Nueva Venta")
        
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_nueva_venta", use_container_width=True):
                st.session_state.seccion_ventas = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
        # Inventario disponible
        total_inventario = inventario_huevos.get("Bodega1_total", 0)
        st.info(f"📦 **Inventario disponible:** {total_inventario:,} huevos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cliente
            clientes_list = [c.get("nombre", "Cliente sin nombre") for c in clientes]
            opciones_clientes = ["➕ Nuevo Cliente"] + clientes_list
            cliente_seleccionado = st.selectbox("👤 Cliente", opciones_clientes, key="cliente_venta")
            
            if cliente_seleccionado == "➕ Nuevo Cliente":
                nuevo_cliente_nombre = st.text_input("Nombre del cliente *")
                nuevo_cliente_telefono = st.text_input("📞 Teléfono")
                nuevo_cliente_direccion = st.text_input("📍 Dirección")
                nuevo_cliente_email = st.text_input("✉️ Email")
            else:
                cliente_info = None
                for c in clientes:
                    if c.get("nombre") == cliente_seleccionado:
                        cliente_info = c
                        break
                if cliente_info:
                    st.write(f"📞 {cliente_info.get('telefono', 'No tiene teléfono')}")
                    st.write(f"📍 {cliente_info.get('direccion', 'No tiene dirección')}")
            
            # Tipo de venta
            tipo_venta = st.selectbox("📋 Tipo de venta", ["Contado", "Crédito", "Pedido"])
            
            # Fecha de entrega (para pedidos)
            if tipo_venta == "Pedido":
                fecha_entrega = st.date_input("📅 Fecha de entrega", datetime.now() + timedelta(days=2))
        
        with col2:
            st.subheader("📦 Detalle de la venta")
            
            # Categorías y cantidades
            clasificacion_venta = {}
            cols = st.columns(2)
            for i, cat in enumerate(categorias.get("categorias", [])):
                with cols[i % 2]:
                    clasificacion_venta[cat] = st.number_input(
                        f"{cat}",
                        min_value=0,
                        value=0,
                        step=50,
                        key=f"venta_{cat}"
                    )
            
            total_huevos_venta = sum(clasificacion_venta.values())
            
            # Precio
            precio_unitario = st.number_input(
                "💰 Precio por unidad ($)",
                min_value=0,
                value=250,
                step=50,
                key="precio_unitario"
            )
            
            # Descuento
            descuento = st.number_input(
                "🏷️ Descuento (%)",
                min_value=0,
                max_value=100,
                value=0,
                step=5,
                key="descuento"
            )
            
            total_bruto = total_huevos_venta * precio_unitario
            total_descuento = total_bruto * (descuento / 100)
            total_venta = total_bruto - total_descuento
            
            st.write("---")
            st.write(f"**📊 Total huevos:** {total_huevos_venta:,}")
            st.write(f"**💰 Subtotal:** ${total_bruto:,.0f}")
            if descuento > 0:
                st.write(f"**🏷️ Descuento:** -${total_descuento:,.0f} ({descuento}%)")
            st.write(f"**💵 Total:** ${total_venta:,.0f}")
        
        # Botón guardar
        st.write("---")
        if st.button("✅ GUARDAR VENTA", type="primary", use_container_width=True):
            # Validaciones
            if total_huevos_venta > total_inventario:
                st.error(f"❌ No hay suficiente inventario. Disponible: {total_inventario:,} huevos")
            elif total_huevos_venta == 0:
                st.error("❌ Debe seleccionar al menos un huevo")
            elif cliente_seleccionado == "➕ Nuevo Cliente" and not nuevo_cliente_nombre:
                st.error("❌ Debe ingresar el nombre del nuevo cliente")
            else:
                # Crear o buscar cliente
                cliente_id = None
                if cliente_seleccionado == "➕ Nuevo Cliente":
                    nuevo_cliente = {
                        "id": len(clientes) + 1,
                        "nombre": nuevo_cliente_nombre,
                        "telefono": nuevo_cliente_telefono,
                        "direccion": nuevo_cliente_direccion,
                        "email": nuevo_cliente_email,
                        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    clientes.append(nuevo_cliente)
                    guardar_clientes(clientes)
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
                    "cliente_nombre": cliente_seleccionado if cliente_seleccionado != "➕ Nuevo Cliente" else nuevo_cliente_nombre,
                    "factura": generar_numero_factura(),
                    "clasificacion": clasificacion_venta,
                    "total_huevos": total_huevos_venta,
                    "precio_unitario": precio_unitario,
                    "descuento": descuento,
                    "total_bruto": total_bruto,
                    "total": total_venta,
                    "tipo": tipo_venta,
                    "estado": "Completada" if tipo_venta != "Pedido" else "Pendiente"
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
    
    # ============================================
    # CLIENTES
    # ============================================
    elif st.session_state.seccion_ventas == "clientes":
        st.title("👥 Gestión de Clientes")
        
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
            nuevo_cliente_nombre = st.text_input("Nombre completo *", key="new_cliente_nombre")
            nuevo_cliente_telefono = st.text_input("📞 Teléfono", key="new_cliente_telefono")
        with col2:
            nuevo_cliente_direccion = st.text_input("📍 Dirección", key="new_cliente_direccion")
            nuevo_cliente_email = st.text_input("✉️ Email", key="new_cliente_email")
        
        if st.button("➕ Agregar Cliente", type="primary"):
            if nuevo_cliente_nombre:
                nuevo_cliente = {
                    "id": len(clientes) + 1,
                    "nombre": nuevo_cliente_nombre,
                    "telefono": nuevo_cliente_telefono,
                    "direccion": nuevo_cliente_direccion,
                    "email": nuevo_cliente_email,
                    "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                clientes.append(nuevo_cliente)
                guardar_clientes(clientes)
                st.success(f"✅ Cliente '{nuevo_cliente_nombre}' agregado correctamente")
                st.rerun()
            else:
                st.error("❌ El nombre del cliente es obligatorio")
    
    # ============================================
    # PEDIDOS
    # ============================================
    elif st.session_state.seccion_ventas == "pedidos":
        st.title("📋 Gestión de Pedidos")
        
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_pedidos", use_container_width=True):
                st.session_state.seccion_ventas = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
        # Filtrar pedidos
        pedidos_ventas = [v for v in ventas if v.get("tipo") == "Pedido"]
        
        if pedidos_ventas:
            # Estados
            estados = ["Todos", "Pendiente", "En preparación", "Entregado"]
            filtro_estado = st.selectbox("Filtrar por estado", estados)
            
            pedidos_filtrados = pedidos_ventas
            if filtro_estado != "Todos":
                pedidos_filtrados = [v for v in pedidos_ventas if v.get("estado") == filtro_estado]
            
            if pedidos_filtrados:
                for p in pedidos_filtrados:
                    cliente = obtener_cliente_por_id(p.get("cliente_id"), clientes)
                    nombre_cliente = cliente.get("nombre", "Cliente no encontrado") if cliente else "Cliente no encontrado"
                    
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{p.get('fecha', '').split(' ')[0]}** - {nombre_cliente}")
                        st.write(f"📦 {p.get('total_huevos', 0):,} huevos")
                    with col2:
                        st.write(f"**Estado:** {p.get('estado', 'Pendiente')}")
                    with col3:
                        st.write(f"**${p.get('total', 0):,.0f}**")
                    
                    # Botones para cambiar estado
                    if p.get('estado') == "Pendiente":
                        if st.button(f"📦 Preparar", key=f"preparar_{p['id']}"):
                            for v in ventas:
                                if v.get("id") == p["id"]:
                                    v["estado"] = "En preparación"
                                    break
                            guardar_ventas(ventas)
                            st.rerun()
                    elif p.get('estado') == "En preparación":
                        if st.button(f"✅ Entregar", key=f"entregar_{p['id']}"):
                            for v in ventas:
                                if v.get("id") == p["id"]:
                                    v["estado"] = "Entregado"
                                    break
                            guardar_ventas(ventas)
                            st.rerun()
                    st.markdown("---")
            else:
                st.info(f"No hay pedidos con estado '{filtro_estado}'")
        else:
            st.info("No hay pedidos registrados aún.")
    
    # ============================================
    # HISTORIAL DE VENTAS
    # ============================================
    elif st.session_state.seccion_ventas == "historial":
        st.title("📊 Historial de Ventas")
        
        col_back, col_spacer = st.columns([1, 5])
        with col_back:
            if st.button("← REGRESAR", key="back_historial", use_container_width=True):
                st.session_state.seccion_ventas = "dashboard"
                st.rerun()
        
        st.markdown("---")
        
        if ventas:
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                fecha_desde = st.date_input("📅 Desde", datetime.now() - timedelta(days=30), key="ventas_desde")
            with col2:
                fecha_hasta = st.date_input("📅 Hasta", datetime.now(), key="ventas_hasta")
            
            fecha_desde_str = fecha_desde.strftime("%Y-%m-%d")
            fecha_hasta_str = fecha_hasta.strftime("%Y-%m-%d")
            
            # Filtrar ventas
            ventas_filtradas = []
            for v in ventas:
                fecha_venta = v.get("fecha", "").split(" ")[0]
                if fecha_desde_str <= fecha_venta <= fecha_hasta_str:
                    ventas_filtradas.append(v)
            
            if ventas_filtradas:
                df_ventas = pd.DataFrame(ventas_filtradas)
                
                # Resumen
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
                
                df_mostrar = df_ventas[["fecha", "cliente_nombre", "factura", "total_huevos", "total", "estado"]]
                df_mostrar = df_mostrar.rename(columns={
                    "fecha": "Fecha",
                    "cliente_nombre": "Cliente",
                    "factura": "Factura",
                    "total_huevos": "Huevos",
                    "total": "Total",
                    "estado": "Estado"
                })
                st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
            else:
                st.info("No hay ventas en el período seleccionado")
        else:
            st.info("No hay ventas registradas aún.")
