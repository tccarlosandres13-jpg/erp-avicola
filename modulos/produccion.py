# ============================================
# MÓDULO: PRODUCCIÓN
# ============================================

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modulos.datos import (
    galpones, inventario_gallinas, produccion, movimientos_gallinas,
    categorias_data, obtener_postura_real_periodo, obtener_mortalidad_periodo,
    registrar_produccion, registrar_movimiento_gallinas
)

def mostrar_produccion():
    
    if 'seccion_produccion' not in st.session_state:
        st.session_state.seccion_produccion = "dashboard"
    
    # ========== DASHBOARD PRINCIPAL ==========
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
        
        # Recargar datos
        from modulos.datos import produccion as prod_data, movimientos_gallinas as mov_data
        produccion_local = prod_data
        movimientos_local = mov_data
        
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
                st.markdown("### Clasificación de huevos")
                
                clasificacion = {}
                cols = st.columns(2)
                for i, cat in enumerate(categorias_data["categorias"]):
                    with cols[i % 2]:
                        clasificacion[cat] = st.number_input(f"{cat}", min_value=0, value=0, step=100, key=f"cat_{cat}")
                
                total_ingresado = sum(clasificacion.values())
                
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
            
            if galpones_activos and 'galpon_seleccionado' in locals():
                gallinas_galpon = galpon_seleccionado["cantidad_gallinas"]
                produccion_esperada = int(gallinas_galpon * 0.9)
                st.info(f"📊 Producción esperada para este galpón (90%): **{produccion_esperada:,}** huevos")
    
    # ========== SECCIÓN: INVENTARIO GALLINAS ==========
    elif st.session_state.seccion_produccion == "inventario":
        st.title("🐔 Inventario de Gallinas")
        
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
