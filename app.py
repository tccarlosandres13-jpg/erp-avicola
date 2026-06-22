# ============================================
# MÓDULO: INICIO (Versión estable)
# ============================================

import streamlit as st
from datetime import datetime
from modulos.datos import produccion, inventario_huevos, inventario_gallinas, movimientos_gallinas, galpones

def mostrar_inicio():
    
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a1a0a 0%, #1a3a1a 40%, #2d5a2d 100%) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Banner
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,214,0,0.12), rgba(255,214,0,0.02));
        border-radius: 24px;
        padding: 30px 35px;
        margin-bottom: 28px;
        border: 1px solid rgba(255,214,0,0.08);
        box-shadow: 0 10px 50px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    ">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
            <div>
                <div style="font-size:34px;font-weight:900;color:#FFD600;letter-spacing:2px;text-shadow:0 0 60px rgba(255,214,0,0.1);">
                    🚀 Doña Dora ERP
                </div>
                <div style="font-size:15px;color:rgba(255,255,255,0.5);margin-top:4px;letter-spacing:1px;">
                    🌟 Sistema de Gestión Avícola - La calidad es nuestro sello
                </div>
            </div>
            <div style="background:rgba(255,214,0,0.06);padding:10px 22px;border-radius:14px;border:1px solid rgba(255,214,0,0.08);">
                <span style="color:#FFD600;font-weight:700;font-size:15px;letter-spacing:1px;">
                    📅 """ + datetime.now().strftime("%d/%m/%Y") + """
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Estadísticas
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    total_inventario = inventario_huevos.get("Bodega1_total", 0)
    total_gallinas = sum(g.get("cantidad", 0) for g in inventario_gallinas.values())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border-radius:18px;padding:22px 24px;border:1px solid rgba(255,255,255,0.05);backdrop-filter:blur(10px);box-shadow:0 8px 30px rgba(0,0,0,0.2);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.35);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Producción Hoy</div>
                    <div style="font-size:36px;font-weight:800;color:#FFD600;margin-top:2px;">{total_hoy:,}</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.25);">🥚 huevos</div>
                </div>
                <div style="background:rgba(255,214,0,0.08);border-radius:50%;width:60px;height:60px;display:flex;align-items:center;justify-content:center;font-size:30px;border:1px solid rgba(255,214,0,0.08);">
                    🥚
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border-radius:18px;padding:22px 24px;border:1px solid rgba(255,255,255,0.05);backdrop-filter:blur(10px);box-shadow:0 8px 30px rgba(0,0,0,0.2);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.35);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Inventario</div>
                    <div style="font-size:36px;font-weight:800;color:#FFD600;margin-top:2px;">{total_inventario:,}</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.25);">📦 huevos</div>
                </div>
                <div style="background:rgba(255,214,0,0.08);border-radius:50%;width:60px;height:60px;display:flex;align-items:center;justify-content:center;font-size:30px;border:1px solid rgba(255,214,0,0.08);">
                    📦
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border-radius:18px;padding:22px 24px;border:1px solid rgba(255,255,255,0.05);backdrop-filter:blur(10px);box-shadow:0 8px 30px rgba(0,0,0,0.2);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.35);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Gallinas</div>
                    <div style="font-size:36px;font-weight:800;color:#FFD600;margin-top:2px;">{total_gallinas:,}</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.25);">🐔 aves</div>
                </div>
                <div style="background:rgba(255,214,0,0.08);border-radius:50%;width:60px;height:60px;display:flex;align-items:center;justify-content:center;font-size:30px;border:1px solid rgba(255,214,0,0.08);">
                    🐔
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== MÓDULOS ==========
    st.markdown("""
    <div style="text-align:center;margin-bottom:22px;">
        <div style="font-size:24px;font-weight:800;color:#FFD600;letter-spacing:3px;text-transform:uppercase;text-shadow:0 0 40px rgba(255,214,0,0.06);">
            📋 Módulos del Sistema
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.25);margin-top:2px;letter-spacing:2px;">
            SELECCIONA UN MÓDULO PARA COMENZAR
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Módulos en 3 columnas
    modulos = [
        {"nombre": "🐔 Producción", "gradient": "linear-gradient(135deg, #2E7D32, #43A047)", "key": "produccion", "desc": "Registro diario de huevos"},
        {"nombre": "💰 Ventas", "gradient": "linear-gradient(135deg, #F9A825, #FFD54F)", "key": "ventas", "desc": "Gestión de ventas"},
        {"nombre": "📦 Inventario", "gradient": "linear-gradient(135deg, #1976D2, #42A5F5)", "key": "inventario", "desc": "Stock en bodega 1"},
        {"nombre": "🏷️ Categorías", "gradient": "linear-gradient(135deg, #7B1FA2, #AB47BC)", "key": "categorias", "desc": "Gestionar categorías"},
        {"nombre": "📊 Reportes", "gradient": "linear-gradient(135deg, #E65100, #FB8C00)", "key": "reportes", "desc": "Ver reportes"},
        {"nombre": "👥 Usuarios", "gradient": "linear-gradient(135deg, #00695C, #00897B)", "key": "usuarios", "desc": "Gestionar usuarios"},
        {"nombre": "⚙️ Configuración", "gradient": "linear-gradient(135deg, #455A64, #78909C)", "key": "configuracion", "desc": "Configurar galpones"},
    ]
    
    for i in range(0, len(modulos), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(modulos):
                mod = modulos[idx]
                with col:
                    # Usar botón normal de Streamlit
                    if st.button(
                        f"{mod['nombre']}\n{mod['desc']}",
                        key=f"card_{mod['key']}",
                        use_container_width=True
                    ):
                        st.session_state.menu_seleccionado = mod['key']
                        st.rerun()
                    
                    # Estilo del botón
                    st.markdown(f"""
                    <style>
                        div[data-testid="stButton"] button[key="card_{mod['key']}"] {{
                            background: {mod['gradient']} !important;
                            color: white !important;
                            border-radius: 20px !important;
                            padding: 30px 10px !important;
                            height: auto !important;
                            min-height: 130px !important;
                            text-align: center !important;
                            font-size: 20px !important;
                            font-weight: 700 !important;
                            box-shadow: 0 10px 40px rgba(0,0,0,0.3) !important;
                            border: 1px solid rgba(255,255,255,0.06) !important;
                            line-height: 2 !important;
                            white-space: pre-line !important;
                            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
                            letter-spacing: 0.5px !important;
                        }}
                        div[data-testid="stButton"] button[key="card_{mod['key']}"]:hover {{
                            transform: translateY(-8px) scale(1.02) !important;
                            box-shadow: 0 20px 60px rgba(0,0,0,0.5) !important;
                        }}
                        div[data-testid="stButton"] button[key="card_{mod['key']}"]:active {{
                            transform: scale(0.95) !important;
                        }}
                    </style>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Últimas producciones
    st.markdown("""
    <div style="background:rgba(255,255,255,0.02);border-radius:18px;padding:20px 26px;border:1px solid rgba(255,255,255,0.04);backdrop-filter:blur(10px);">
        <div style="font-size:17px;font-weight:700;color:#FFD600;margin-bottom:12px;display:flex;align-items:center;gap:10px;">
            📈 Últimas producciones
        </div>
    """, unsafe_allow_html=True)
    
    if produccion:
        ultimas = produccion[-5:][::-1]
        for p in ultimas:
            galpon_nombre = next((g["nombre"] for g in galpones if g["id"] == p["galpon_id"]), "Desconocido")
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:10px 16px;margin-bottom:4px;border-left:3px solid #FFD600;">
                <span style="font-weight:600;color:#FFD600;">{p['fecha']}</span>
                <span style="color:rgba(255,255,255,0.4);"> - {galpon_nombre}:</span>
                <span style="font-weight:600;color:#FFD600;">{p['total_huevos']:,}</span>
                <span style="color:rgba(255,255,255,0.3);"> huevos</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No hay registros de producción aún.")
    
    st.markdown("</div>", unsafe_allow_html=True)
