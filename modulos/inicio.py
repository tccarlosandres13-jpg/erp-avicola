# ============================================
# MÓDULO: INICIO (Diseño Premium - Estilo JARVIS)
# ============================================

import streamlit as st
from datetime import datetime
from modulos.datos import produccion, inventario_huevos, inventario_gallinas, movimientos_gallinas, galpones

def mostrar_inicio():
    
    # Fondo con efecto premium
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a1a0a 0%, #1a3a1a 40%, #2d5a2d 100%) !important;
        }
        .stDataFrame {
            background: rgba(255,255,255,0.05) !important;
            border-radius: 16px !important;
        }
        .stAlert {
            background: rgba(255,255,255,0.05) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ========== BANNER SUPERIOR ==========
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,214,0,0.12), rgba(255,214,0,0.02));
        border-radius: 24px;
        padding: 35px 40px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,214,0,0.10);
        box-shadow: 0 10px 50px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <div style="
                    font-size: 36px;
                    font-weight: 900;
                    color: #FFD600;
                    letter-spacing: 2px;
                    text-shadow: 0 0 60px rgba(255,214,0,0.15);
                ">
                    🚀 Doña Dora ERP
                </div>
                <div style="
                    font-size: 16px;
                    color: rgba(255,255,255,0.6);
                    margin-top: 6px;
                    font-weight: 400;
                    letter-spacing: 1px;
                ">
                    🌟 Sistema de Gestión Avícola - La calidad es nuestro sello de identidad
                </div>
            </div>
            <div style="
                background: rgba(255,214,0,0.08);
                padding: 12px 24px;
                border-radius: 16px;
                border: 1px solid rgba(255,214,0,0.12);
            ">
                <span style="color: #FFD600; font-weight: 700; font-size: 16px; letter-spacing: 1px;">
                    📅 """ + datetime.now().strftime("%d/%m/%Y") + """
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== TARJETAS DE ESTADÍSTICAS ==========
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    total_inventario = inventario_huevos.get("Bodega1_total", 0)
    total_gallinas = sum(g.get("cantidad", 0) for g in inventario_gallinas.values())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.04);
            border-radius: 20px;
            padding: 24px 26px;
            border: 1px solid rgba(255,255,255,0.06);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.4);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Producción Hoy</div>
                    <div style="font-size:38px;font-weight:800;color:#FFD600;margin-top:4px;">{total_hoy:,}</div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.3);">🥚 huevos</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, rgba(255,214,0,0.15), rgba(255,214,0,0.05));
                    border-radius: 50%;
                    width: 65px;
                    height: 65px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:32px;
                    border: 1px solid rgba(255,214,0,0.15);
                    box-shadow: 0 0 40px rgba(255,214,0,0.05);
                ">
                    🥚
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.04);
            border-radius: 20px;
            padding: 24px 26px;
            border: 1px solid rgba(255,255,255,0.06);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.4);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Inventario</div>
                    <div style="font-size:38px;font-weight:800;color:#FFD600;margin-top:4px;">{total_inventario:,}</div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.3);">📦 huevos</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, rgba(255,214,0,0.15), rgba(255,214,0,0.05));
                    border-radius: 50%;
                    width: 65px;
                    height: 65px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:32px;
                    border: 1px solid rgba(255,214,0,0.15);
                    box-shadow: 0 0 40px rgba(255,214,0,0.05);
                ">
                    📦
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.04);
            border-radius: 20px;
            padding: 24px 26px;
            border: 1px solid rgba(255,255,255,0.06);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.4);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Gallinas</div>
                    <div style="font-size:38px;font-weight:800;color:#FFD600;margin-top:4px;">{total_gallinas:,}</div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.3);">🐔 aves</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, rgba(255,214,0,0.15), rgba(255,214,0,0.05));
                    border-radius: 50%;
                    width: 65px;
                    height: 65px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:32px;
                    border: 1px solid rgba(255,214,0,0.15);
                    box-shadow: 0 0 40px rgba(255,214,0,0.05);
                ">
                    🐔
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== MÓDULOS ==========
    st.markdown("""
    <div style="text-align:center;margin-bottom:25px;">
        <div style="font-size:26px;font-weight:800;color:#FFD600;letter-spacing:3px;text-transform:uppercase;text-shadow:0 0 40px rgba(255,214,0,0.1);">
            📋 Módulos del Sistema
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.3);margin-top:4px;letter-spacing:2px;">
            SELECCIONA UN MÓDULO PARA COMENZAR
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Módulos con colores vibrantes
    modulos = [
        {"nombre": "🐔 Producción", "gradient": "linear-gradient(135deg, #2E7D32, #43A047)", "key": "produccion", "desc": "Registro diario de huevos"},
        {"nombre": "💰 Ventas", "gradient": "linear-gradient(135deg, #F9A825, #FFD54F)", "key": "ventas", "desc": "Gestión de ventas"},
        {"nombre": "📦 Inventario", "gradient": "linear-gradient(135deg, #1976D2, #42A5F5)", "key": "inventario", "desc": "Stock en bodega 1"},
        {"nombre": "🏷️ Categorías", "gradient": "linear-gradient(135deg, #7B1FA2, #AB47BC)", "key": "categorias", "desc": "Gestionar categorías"},
        {"nombre": "📊 Reportes", "gradient": "linear-gradient(135deg, #E65100, #FB8C00)", "key": "reportes", "desc": "Ver reportes"},
        {"nombre": "👥 Usuarios", "gradient": "linear-gradient(135deg, #00695C, #00897B)", "key": "usuarios", "desc": "Gestionar usuarios"},
        {"nombre": "⚙️ Configuración", "gradient": "linear-gradient(135deg, #455A64, #78909C)", "key": "configuracion", "desc": "Configurar galpones"},
    ]
    
    # Mostrar en filas de 3 con botones grandes
    for i in range(0, len(modulos), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(modulos):
                mod = modulos[idx]
                with col:
                    if st.button(
                        f"{mod['nombre']}\n{mod['desc']}",
                        key=f"card_{mod['key']}",
                        use_container_width=True
                    ):
                        st.session_state.menu_seleccionado = mod['key']
                        st.rerun()
                    
                    st.markdown(f"""
                    <style>
                        div[data-testid="stButton"] button[key="card_{mod['key']}"] {{
                            background: {mod['gradient']} !important;
                            color: white !important;
                            border-radius: 20px !important;
                            padding: 35px 10px !important;
                            height: auto !important;
                            min-height: 140px !important;
                            text-align: center !important;
                            font-size: 22px !important;
                            font-weight: 700 !important;
                            box-shadow: 0 10px 40px rgba(0,0,0,0.3) !important;
                            border: 1px solid rgba(255,255,255,0.08) !important;
                            line-height: 2.2 !important;
                            white-space: pre-line !important;
                            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
                            letter-spacing: 0.5px !important;
                            backdrop-filter: blur(10px) !important;
                            text-shadow: 0 2px 20px rgba(0,0,0,0.2) !important;
                        }}
                        div[data-testid="stButton"] button[key="card_{mod['key']}"]:hover {{
                            transform: translateY(-10px) scale(1.03) !important;
                            box-shadow: 0 20px 60px rgba(0,0,0,0.5) !important;
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
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
        padding: 22px 28px;
        border: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    ">
        <div style="font-size:18px;font-weight:700;color:#FFD600;margin-bottom:14px;display:flex;align-items:center;gap:12px;">
            <span style="font-size:24px;">📈</span> Últimas producciones
        </div>
    """, unsafe_allow_html=True)
    
    if produccion:
        ultimas = produccion[-5:][::-1]
        for p in ultimas:
            galpon_nombre = next((g["nombre"] for g in galpones if g["id"] == p["galpon_id"]), "Desconocido")
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.04);
                border-radius: 12px;
                padding: 12px 18px;
                margin-bottom: 6px;
                border-left: 3px solid #FFD600;
            ">
                <span style="font-weight:600;color:#FFD600;">{p['fecha']}</span>
                <span style="color:rgba(255,255,255,0.5);"> - {galpon_nombre}:</span>
                <span style="font-weight:600;color:#FFD600;">{p['total_huevos']:,}</span>
                <span style="color:rgba(255,255,255,0.3);"> huevos</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No hay registros de producción aún.")
    
    st.markdown("</div>", unsafe_allow_html=True)
