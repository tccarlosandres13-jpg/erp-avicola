# ============================================
# MÓDULO: INICIO (Diseño moderno y vibrante)
# ============================================

import streamlit as st
from datetime import datetime
from modulos.datos import produccion, inventario_huevos, inventario_gallinas, movimientos_gallinas, galpones

def mostrar_inicio():
    
    # ========== BANNER SUPERIOR ==========
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        border-radius: 20px;
        padding: 35px 40px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(46, 125, 50, 0.3);
        border: 1px solid rgba(255, 214, 0, 0.15);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <div style="
                    font-size: 32px;
                    font-weight: 900;
                    color: white;
                    letter-spacing: 1px;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
                ">
                    🏠 Doña Dora ERP
                </div>
                <div style="
                    font-size: 16px;
                    color: #A5D6A7;
                    margin-top: 6px;
                    font-weight: 500;
                    letter-spacing: 0.5px;
                ">
                    🌟 Sistema de Gestión Avícola - La calidad es nuestro sello de identidad
                </div>
            </div>
            <div style="
                background: rgba(255, 214, 0, 0.12);
                padding: 12px 22px;
                border-radius: 14px;
                border: 1px solid rgba(255, 214, 0, 0.2);
                backdrop-filter: blur(10px);
            ">
                <span style="color: #FFD600; font-weight: 700; font-size: 15px; letter-spacing: 1px;">
                    📅 """ + datetime.now().strftime("%d/%m/%Y") + """
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== TARJETAS DE ESTADÍSTICAS (3D) ==========
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    total_inventario = inventario_huevos.get("Bodega1_total", 0)
    total_gallinas = sum(g.get("cantidad", 0) for g in inventario_gallinas.values())
    
    col1, col2, col3 = st.columns(3)
    
    # Tarjeta 1: Producción
    with col1:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border-left: 6px solid #2E7D32;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 12px; color: #888; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;">Producción Hoy</div>
                    <div style="font-size: 34px; font-weight: 800; color: #2E7D32; margin-top: 4px;">{total_hoy:,}</div>
                    <div style="font-size: 12px; color: #aaa; margin-top: 2px;">🥚 huevos</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, #2E7D32, #388E3C);
                    border-radius: 50%;
                    width: 55px;
                    height: 55px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 28px;
                    box-shadow: 0 4px 15px rgba(46,125,50,0.2);
                ">
                    🥚
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tarjeta 2: Inventario
    with col2:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border-left: 6px solid #F9A825;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 12px; color: #888; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;">Inventario Bodega 1</div>
                    <div style="font-size: 34px; font-weight: 800; color: #F9A825; margin-top: 4px;">{total_inventario:,}</div>
                    <div style="font-size: 12px; color: #aaa; margin-top: 2px;">📦 huevos</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, #F9A825, #FFC107);
                    border-radius: 50%;
                    width: 55px;
                    height: 55px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 28px;
                    box-shadow: 0 4px 15px rgba(249,168,37,0.2);
                ">
                    📦
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tarjeta 3: Gallinas
    with col3:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border-left: 6px solid #1B5E20;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 12px; color: #888; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;">Gallinas Vivas</div>
                    <div style="font-size: 34px; font-weight: 800; color: #1B5E20; margin-top: 4px;">{total_gallinas:,}</div>
                    <div style="font-size: 12px; color: #aaa; margin-top: 2px;">🐔 aves</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, #1B5E20, #2E7D32);
                    border-radius: 50%;
                    width: 55px;
                    height: 55px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 28px;
                    box-shadow: 0 4px 15px rgba(27,94,32,0.2);
                ">
                    🐔
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== MÓDULOS (TARJETAS GRANDES CON BOTONES) ==========
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <div style="
            font-size: 24px;
            font-weight: 800;
            color: #2E7D32;
            letter-spacing: 2px;
            text-transform: uppercase;
        ">
            📋 Módulos del Sistema
        </div>
        <div style="
            font-size: 14px;
            color: #999;
            margin-top: 4px;
            font-weight: 400;
        ">
            Selecciona un módulo para comenzar a trabajar
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Definir módulos con colores y emojis
    modulos = [
        {"nombre": "🐔 Producción", "color": "#2E7D32", "key": "produccion", "desc": "Registro diario de huevos", "bg": "linear-gradient(135deg, #2E7D32, #43A047)"},
        {"nombre": "💰 Ventas", "color": "#F9A825", "key": "ventas", "desc": "Gestión de ventas y clientes", "bg": "linear-gradient(135deg, #F9A825, #FFD54F)"},
        {"nombre": "📦 Inventario", "color": "#1976D2", "key": "inventario", "desc": "Stock en bodega 1", "bg": "linear-gradient(135deg, #1976D2, #42A5F5)"},
        {"nombre": "🏷️ Categorías", "color": "#7B1FA2", "key": "categorias", "desc": "Gestionar categorías", "bg": "linear-gradient(135deg, #7B1FA2, #AB47BC)"},
        {"nombre": "📊 Reportes", "color": "#E65100", "key": "reportes", "desc": "Ver reportes de producción", "bg": "linear-gradient(135deg, #E65100, #FB8C00)"},
        {"nombre": "👥 Usuarios", "color": "#00695C", "key": "usuarios", "desc": "Gestionar usuarios", "bg": "linear-gradient(135deg, #00695C, #00897B)"},
        {"nombre": "⚙️ Configuración", "color": "#455A64", "key": "configuracion", "desc": "Configurar galpones", "bg": "linear-gradient(135deg, #455A64, #78909C)"},
    ]
    
    # Mostrar en filas de 3
    for i in range(0, len(modulos), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(modulos):
                mod = modulos[idx]
                with col:
                    # Botón con diseño moderno
                    if st.button(
                        f"{mod['nombre']}\n{mod['desc']}",
                        key=f"card_{mod['key']}",
                        use_container_width=True
                    ):
                        st.session_state.menu_seleccionado = mod['key']
                        st.rerun()
                    
                    # Estilo moderno con gradiente y efectos
                    st.markdown(f"""
                    <style>
                        div[data-testid="stButton"] button[key="card_{mod['key']}"] {{
                            background: {mod['bg']} !important;
                            color: white !important;
                            border-radius: 18px !important;
                            padding: 30px 10px !important;
                            height: auto !important;
                            min-height: 130px !important;
                            text-align: center !important;
                            font-size: 20px !important;
                            font-weight: 700 !important;
                            box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
                            border: none !important;
                            line-height: 2 !important;
                            white-space: pre-line !important;
                            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
                            letter-spacing: 0.5px !important;
                        }}
                        div[data-testid="stButton"] button[key="card_{mod['key']}"]:hover {{
                            transform: translateY(-8px) scale(1.02) !important;
                            box-shadow: 0 16px 50px rgba(0,0,0,0.25) !important;
                        }}
                        div[data-testid="stButton"] button[key="card_{mod['key']}"]:active {{
                            transform: scale(0.95) !important;
                        }}
                    </style>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== ÚLTIMAS PRODUCCIONES ==========
    st.markdown("""
    <div style="
        background: white;
        border-radius: 18px;
        padding: 22px 28px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.02);
    ">
        <div style="
            font-size: 18px;
            font-weight: 700;
            color: #2E7D32;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <span style="font-size: 24px;">📈</span> Últimas producciones registradas
        </div>
    """, unsafe_allow_html=True)
    
    if produccion:
        ultimas = produccion[-5:][::-1]
        for p in ultimas:
            galpon_nombre = next((g["nombre"] for g in galpones if g["id"] == p["galpon_id"]), "Desconocido")
            st.markdown(f"""
            <div style="
                background: #f8faf8;
                border-radius: 10px;
                padding: 10px 16px;
                margin-bottom: 6px;
                border-left: 3px solid #2E7D32;
            ">
                <span style="font-weight: 600; color: #2E7D32;">{p['fecha']}</span>
                <span style="color: #555;"> - {galpon_nombre}:</span>
                <span style="font-weight: 600; color: #1B5E20;">{p['total_huevos']:,}</span>
                <span style="color: #888;"> huevos</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No hay registros de producción aún. Comienza registrando tu primera producción.")
    
    st.markdown("</div>", unsafe_allow_html=True)
