# ============================================
# MÓDULO: INICIO (Con mejor contraste)
# ============================================

import streamlit as st
from datetime import datetime
from modulos.datos import produccion, inventario_huevos, inventario_gallinas, galpones

def mostrar_inicio():
    
    # Banner superior
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,214,0,0.10), rgba(255,214,0,0.02));
        border-radius: 24px;
        padding: 32px 38px;
        margin-bottom: 28px;
        border: 1px solid rgba(255,214,0,0.06);
        box-shadow: 0 10px 50px rgba(0,0,0,0.3);
    ">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
            <div>
                <div style="font-size:36px;font-weight:900;color:#FFD600;letter-spacing:2px;text-shadow:0 0 60px rgba(255,214,0,0.05);">
                    🚀 Doña Dora ERP
                </div>
                <div style="font-size:16px;color:rgba(255,255,255,0.4);margin-top:6px;letter-spacing:1px;font-weight:400;">
                    🌟 Sistema de Gestión Avícola - La calidad es nuestro sello
                </div>
            </div>
            <div style="background:rgba(255,214,0,0.06);padding:12px 24px;border-radius:14px;border:1px solid rgba(255,214,0,0.08);">
                <span style="color:#FFD600;font-weight:700;font-size:16px;letter-spacing:1px;">
                    📅 """ + datetime.now().strftime("%d/%m/%Y") + """
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== ESTADÍSTICAS ==========
    hoy = datetime.now().strftime("%Y-%m-%d")
    produccion_hoy = [p for p in produccion if p["fecha"] == hoy]
    total_hoy = sum(p["total_huevos"] for p in produccion_hoy) if produccion_hoy else 0
    total_inventario = inventario_huevos.get("Bodega1_total", 0)
    total_gallinas = sum(g.get("cantidad", 0) for g in inventario_gallinas.values())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border-radius:18px;padding:24px 26px;border:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.3);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Producción Hoy</div>
                    <div style="font-size:38px;font-weight:800;color:#FFD600;margin-top:2px;">{total_hoy:,}</div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.25);">🥚 huevos</div>
                </div>
                <div style="background:rgba(255,214,0,0.08);border-radius:50%;width:65px;height:65px;display:flex;align-items:center;justify-content:center;font-size:32px;border:1px solid rgba(255,214,0,0.08);">
                    🥚
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border-radius:18px;padding:24px 26px;border:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.3);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Inventario</div>
                    <div style="font-size:38px;font-weight:800;color:#FFD600;margin-top:2px;">{total_inventario:,}</div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.25);">📦 huevos</div>
                </div>
                <div style="background:rgba(255,214,0,0.08);border-radius:50%;width:65px;height:65px;display:flex;align-items:center;justify-content:center;font-size:32px;border:1px solid rgba(255,214,0,0.08);">
                    📦
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border-radius:18px;padding:24px 26px;border:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.3);font-weight:600;letter-spacing:2px;text-transform:uppercase;">Gallinas</div>
                    <div style="font-size:38px;font-weight:800;color:#FFD600;margin-top:2px;">{total_gallinas:,}</div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.25);">🐔 aves</div>
                </div>
                <div style="background:rgba(255,214,0,0.08);border-radius:50%;width:65px;height:65px;display:flex;align-items:center;justify-content:center;font-size:32px;border:1px solid rgba(255,214,0,0.08);">
                    🐔
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== MENSAJE PARA USAR MENÚ LATERAL ==========
    st.markdown("""
    <div style="text-align:center;padding:20px 0;">
        <div style="font-size:18px;font-weight:600;color:rgba(255,255,255,0.2);letter-spacing:3px;text-transform:uppercase;">
            📋 Utiliza el menú lateral para navegar
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.12);margin-top:4px;letter-spacing:2px;">
            SELECCIONA UN MÓDULO EN EL PANEL IZQUIERDO
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== ÚLTIMAS PRODUCCIONES ==========
    st.markdown("""
    <div style="background:rgba(255,255,255,0.02);border-radius:18px;padding:22px 28px;border:1px solid rgba(255,255,255,0.04);">
        <div style="font-size:18px;font-weight:700;color:#FFD600;margin-bottom:14px;display:flex;align-items:center;gap:12px;">
            📈 Últimas producciones
        </div>
    """, unsafe_allow_html=True)
    
    if produccion:
        ultimas = produccion[-5:][::-1]
        for p in ultimas:
            galpon_nombre = next((g["nombre"] for g in galpones if g["id"] == p["galpon_id"]), "Desconocido")
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:12px 18px;margin-bottom:6px;border-left:3px solid #FFD600;">
                <span style="font-weight:600;color:#FFD600;">{p['fecha']}</span>
                <span style="color:rgba(255,255,255,0.4);"> - {galpon_nombre}:</span>
                <span style="font-weight:600;color:#FFD600;">{p['total_huevos']:,}</span>
                <span style="color:rgba(255,255,255,0.3);"> huevos</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No hay registros de producción aún.")
    
    st.markdown("</div>", unsafe_allow_html=True)
