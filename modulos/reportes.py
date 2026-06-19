# ============================================
# MÓDULO: REPORTES
# ============================================

import streamlit as st
import pandas as pd
from modulos.datos import produccion, galpones

def mostrar_reportes():
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
