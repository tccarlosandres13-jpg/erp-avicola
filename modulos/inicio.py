# ============================================
# MÓDULO: INICIO (Menú Principal Profesional)
# ============================================

import streamlit as st
from datetime import datetime
from modulos.datos import produccion, inventario_huevos, inventario_gallinas, movimientos_gallinas, galpones

def mostrar_inicio():
    
    # ========== ENCABEZADO PROFESIONAL ==========
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        border-radius: 20px;
        padding: 30px 35px;
        margin-bottom: 30px;
        box-shadow: 0 8px 30px rgba(46, 125, 50, 0.25);
        border: 1px solid rgba(255, 214, 0, 0.2);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="
                    font-size: 28px;
                    font-weight: 900;
                    color: white;
                    letter-spacing: 1px;
                ">
                    🏠 Bienvenido a Doña Dora ERP
                </div>
                <div style="
                    font-size: 14px;
                    color: #A5D6A7;
                    margin-top: 6px;
                    font-weight: 500;
                ">
                    🌟 Sistema de Gestión Avícola - La calidad es nuestro sello de identidad
                </div>
            </div>
            <div style="
                background: rgba(255, 214, 0, 0.15);
                padding: 10px 18px;
                border-radius: 12px;
                border: 1px solid rgba(255, 214, 0, 0.3);
            ">
                <span style="color: #FFD600; font-weight: 700; font-size: 14px;">
                    📅 """ + datetime.now().strftime("%d/%m/%Y") + """
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== TARJETAS DE ESTADÍSTICAS RÁPIDAS ==========
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    total_inventario = inventario_huevos.get("Bodega1_total", 0)
    total_gallinas = sum(g.get("cantidad", 0) for g in inventario_gallinas.values())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #2E7D32;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 12px; color: #888; font-weight: 600;">PRODUCCIÓN HOY</div>
                    <div style="font-size: 26px; font-weight: 700; color: #2E7D32;">{total_hoy:,}</div>
                </div>
                <div style="font-size: 32px;">🥚</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #F9A825;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 12px; color: #888; font-weight: 600;">INVENTARIO BODEGA 1</div>
                    <div style="font-size: 26px; font-weight: 700; color: #F9A825;">{total_inventario:,}</div>
                </div>
                <div style="font-size: 32px;">📦</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #1B5E20;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 12px; color: #888; font-weight: 600;">GALLINAS VIVAS</div>
                    <div style="font-size: 26px; font-weight: 700; color: #1B5E20;">{total_gallinas:,}</div>
                </div>
                <div style="font-size: 32px;">🐔</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== TÍTULO DE MÓDULOS ==========
    st.markdown("""
    <div style="
        text-align: center;
        margin-bottom: 25px;
    ">
        <div style="
            font-size: 22px;
            font-weight: 700;
            color: #2E7D32;
            letter-spacing: 1px;
        ">
            📋 MÓDULOS DEL SISTEMA
        </div>
        <div style="
            font-size: 13px;
            color: #888;
            margin-top: 4px;
        ">
            Selecciona un módulo para comenzar a trabajar
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== TARJETAS DE MÓDULOS (BOTONES) ==========
    modulos = [
        {"nombre": "Producción", "icono": "🐔", "color": "#2E7D32", "key": "produccion", "desc": "Registro diario de huevos"},
        {"nombre": "Ventas", "icono": "💰", "color": "#F9A825", "key": "ventas", "desc": "Gestión de ventas y clientes"},
        {"nombre": "Inventario", "icono": "📦", "color": "#1976D2", "key": "inventario", "desc": "Stock en bodega 1"},
        {"nombre": "Categorías", "icono": "🏷️", "color": "#7B1FA2", "key": "categorias", "desc": "Gestionar categorías"},
        {"nombre": "Reportes", "icono": "📊", "color": "#E65100", "key": "reportes", "desc": "Ver reportes de producción"},
        {"nombre": "Usuarios", "icono": "👥", "color": "#00695C", "key": "usuarios", "desc": "Gestionar usuarios"},
        {"nombre": "Configuración", "icono": "⚙️", "color": "#455A64", "key": "configuracion", "desc": "Configurar galpones"},
    ]
    
    # Mostrar en filas de 3
    for i in range(0, len(modulos), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(modulos):
                mod = modulos[idx]
                with col:
                    # Estilo de tarjeta con hover
                    st.markdown(f"""
                    <style>
                        div[data-testid="stButton"] button[key="card_{mod['key']}"] {{
                            background: white !important;
                            color: {mod['color']} !important;
                            border-radius: 16px !important;
                            padding: 22px 10px !important;
                            height: auto !important;
                            min-height: 120px !important;
                            text-align: center !important;
                            font-size: 15px !important;
                            font-weight: 700 !important;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.06) !important;
                            border: 2px solid #f0f0f0 !important;
                            transition: all 0.3s ease !important;
                            line-height: 1.6 !important;
                            white-space: pre-line !important;
                        }}
                        div[data-testid="stButton"] button[key="card_{mod['key']}"]:hover {{
                            transform: translateY(-5px) !important;
                            box-shadow: 0 12px 40px rgba(0,0,0,0.10) !important;
                            border-color: {mod['color']} !important;
                            background: linear-gradient(135deg, {mod['color']}10, white) !important;
                        }}
                    </style>
                    """, unsafe_allow_html=True)
                    
                    if st.button(
                        f"{mod['icono']}\n{mod['nombre']}\n{mod['desc']}",
                        key=f"card_{mod['key']}",
                        use_container_width=True,
                        help=f"Ir a {mod['nombre']}"
                    ):
                        st.session_state.menu_seleccionado = mod['key']
                        st.rerun()
    
    st.markdown("---")
    
    # ========== ÚLTIMAS PRODUCCIONES ==========
    st.markdown("""
    <div style="
        background: white;
        border-radius: 16px;
        padding: 20px 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    ">
        <div style="font-size: 16px; font-weight: 700; color: #2E7D32; margin-bottom: 12px;">
            📈 Últimas producciones registradas
        </div>
    """, unsafe_allow_html=True)
    
    if produccion:
        ultimas = produccion[-5:][::-1]
        for p in ultimas:
            galpon_nombre = next((g["nombre"] for g in galpones if g["id"] == p["galpon_id"]), "Desconocido")
            st.write(f"**{p['fecha']}** - {galpon_nombre}: {p['total_huevos']:,} huevos")
    else:
        st.info("No hay registros de producción aún.")
    
    st.markdown("</div>", unsafe_allow_html=True)
