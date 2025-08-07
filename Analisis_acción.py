# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# ------------------- CONFIGURACIÓN INICIAL -------------------
st.set_page_config(page_title="Analizador de Acciones", layout="wide", page_icon="📈")
st.title("📈 Analizador Fundamental de Acciones")
st.markdown("Herramienta para estimar el valor intrínseco de una acción usando modelos de valoración.")

# ------------------- FUNCIÓN PRINCIPAL -------------------
def calcular_valoracion(datos):
    precio_actual = datos['precio_actual']
    resultados = {'calculos': {}}

    if datos.get('eps_estimado', 0) > 0:
        resultados['calculos']['pe'] = {
            'objetivo_pesimista': datos['eps_estimado'] * datos['pe_pesimista'],
            'objetivo_base': datos['eps_estimado'] * datos['pe_base'],
            'objetivo_optimista': datos['eps_estimado'] * datos['pe_optimista'],
        }

    if datos.get('ingresos_por_accion', 0) > 0:
        resultados['calculos']['ps'] = {
            'objetivo_pesimista': datos['ingresos_por_accion'] * datos['ps_pesimista'],
            'objetivo_base': datos['ingresos_por_accion'] * datos['ps_base'],
            'objetivo_optimista': datos['ingresos_por_accion'] * datos['ps_optimista'],
        }

    if datos.get('valor_contable_por_accion', 0) > 0:
        resultados['calculos']['pb'] = {
            'objetivo_pesimista': datos['valor_contable_por_accion'] * datos['pb_pesimista'],
            'objetivo_base': datos['valor_contable_por_accion'] * datos['pb_base'],
            'objetivo_optimista': datos['valor_contable_por_accion'] * datos['pb_optimista'],
        }

    for model, calcs in resultados['calculos'].items():
        calcs['upside_pesimista'] = (calcs['objetivo_pesimista'] / precio_actual - 1) * 100
        calcs['upside_base'] = (calcs['objetivo_base'] / precio_actual - 1) * 100
        calcs['upside_optimista'] = (calcs['objetivo_optimista'] / precio_actual - 1) * 100

    adicionales = {}
    if datos.get('dividendo_anual', 0) > 0 and precio_actual > 0:
        adicionales['rendimiento_dividendo'] = (datos['dividendo_anual'] / precio_actual) * 100

    if 'pe' in resultados['calculos']:
        pe = resultados['calculos']['pe']
        upside_base = pe['upside_base']
        downside_pesimista = abs(pe['upside_pesimista'])

        if downside_pesimista > 0:
            adicionales['riesgo_beneficio'] = upside_base / downside_pesimista

        if datos.get('margen_seguridad', 0) > 0:
            factor = 1 - (datos['margen_seguridad'] / 100)
            adicionales['objetivo_con_margen'] = pe['objetivo_base'] * factor

    resultados['calculos']['adicionales'] = adicionales
    return resultados

# ------------------- INTERFAZ -------------------
st.sidebar.header("📋 Parámetros de Entrada")

ticker = st.sidebar.text_input("Ticker o Empresa", "AAPL").upper()
precio_actual = st.sidebar.number_input("Precio Actual ($)", min_value=0.01, value=170.0, step=0.01)

st.sidebar.subheader("📐 Modelos de Valoración")

with st.sidebar.expander("P/E (Price to Earnings)"):
    eps_estimado = st.number_input("EPS Estimado", min_value=0.0, value=6.5, step=0.01)
    pe_pesimista = st.number_input("P/E Pesimista", min_value=0.1, value=18.0) if eps_estimado > 0 else 0
    pe_base = st.number_input("P/E Base", min_value=0.1, value=25.0) if eps_estimado > 0 else 0
    pe_optimista = st.number_input("P/E Optimista", min_value=0.1, value=30.0) if eps_estimado > 0 else 0

with st.sidebar.expander("P/S (Price to Sales)"):
    ingresos_por_accion = st.number_input("Ingresos por Acción", min_value=0.0, value=25.0, step=0.1)
    ps_pesimista = st.number_input("P/S Pesimista", min_value=0.1, value=5.0) if ingresos_por_accion > 0 else 0
    ps_base = st.number_input("P/S Base", min_value=0.1, value=7.0) if ingresos_por_accion > 0 else 0
    ps_optimista = st.number_input("P/S Optimista", min_value=0.1, value=9.0) if ingresos_por_accion > 0 else 0

with st.sidebar.expander("P/B (Price to Book)"):
    valor_contable_por_accion = st.number_input("Valor Contable por Acción", min_value=0.0, value=4.0, step=0.1)
    pb_pesimista = st.number_input("P/B Pesimista", min_value=0.1, value=20.0) if valor_contable_por_accion > 0 else 0
    pb_base = st.number_input("P/B Base", min_value=0.1, value=35.0) if valor_contable_por_accion > 0 else 0
    pb_optimista = st.number_input("P/B Optimista", min_value=0.1, value=45.0) if valor_contable_por_accion > 0 else 0

st.sidebar.subheader("Parámetros Adicionales")
dividendo_anual = st.sidebar.number_input("Dividendo Anual por Acción ($)", min_value=0.0, value=0.96, step=0.01)
margen_seguridad = st.sidebar.slider("Margen de Seguridad Deseado (%)", 0, 50, 15)

# --- BOTÓN en área principal ---
if st.button("📊 Analizar Acción"):
    datos_entrada = {
        'ticker': ticker,
        'precio_actual': precio_actual,
        'eps_estimado': eps_estimado,
        'pe_pesimista': pe_pesimista if eps_estimado > 0 else 0,
        'pe_base': pe_base if eps_estimado > 0 else 0,
        'pe_optimista': pe_optimista if eps_estimado > 0 else 0,
        'ingresos_por_accion': ingresos_por_accion,
        'ps_pesimista': ps_pesimista if ingresos_por_accion > 0 else 0,
        'ps_base': ps_base if ingresos_por_accion > 0 else 0,
        'ps_optimista': ps_optimista if ingresos_por_accion > 0 else 0,
        'valor_contable_por_accion': valor_contable_por_accion,
        'pb_pesimista': pb_pesimista if valor_contable_por_accion > 0 else 0,
        'pb_base': pb_base if valor_contable_por_accion > 0 else 0,
        'pb_optimista': pb_optimista if valor_contable_por_accion > 0 else 0,
        'dividendo_anual': dividendo_anual,
        'margen_seguridad': margen_seguridad
    }

    resultados = calcular_valoracion(datos_entrada)
    
    st.header(f"Resultados del Análisis para {ticker}")

    # Mostrar métricas clave
    adicionales = resultados['calculos'].get('adicionales', {})
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Precio Actual", value=f"${precio_actual:,.2f}")

    with col2:
        div_yield = adicionales.get('rendimiento_dividendo', 0)
        st.metric(label="Rendimiento por Dividendo", value=f"{div_yield:.2f}%")

    with col3:
        rr_ratio = adicionales.get('riesgo_beneficio')
        if rr_ratio:
            st.metric(label="Ratio Riesgo/Beneficio (P/E)", value=f"{rr_ratio:.2f}",
                      help="Calculado como Potencial Base / Riesgo Pesimista. Un valor > 1.5 es bueno.")

    if margen_seguridad > 0 and 'objetivo_con_margen' in adicionales:
        st.success(f"**Precio de Compra con {margen_seguridad}% de Margen:** ${adicionales['objetivo_con_margen']:,.2f}")

    # Mostrar tablas de resultados
    for model_key, model_name in [('pe', 'P/E'), ('ps', 'P/S'), ('pb', 'P/B')]:
        if model_key in resultados['calculos']:
            st.subheader(f"Análisis por Múltiplo {model_name}")
            calcs = resultados['calculos'][model_key]

            data_dict = {
                "Escenario": ["Pesimista", "Base", "Optimista"],
                "Precio Objetivo ($)": [calcs['objetivo_pesimista'], calcs['objetivo_base'], calcs['objetivo_optimista']],
                "Potencial (%)": [calcs['upside_pesimista'], calcs['upside_base'], calcs['upside_optimista']]
            }
            
            df = pd.DataFrame(data_dict)
            # Color condicional simple en tabla
            def color_potential(val):
                color = 'green' if val >= 0 else 'red'
                return f'color: {color}; font-weight: bold;'
            
            st.dataframe(df.style.applymap(color_potential, subset=['Potencial (%)']), use_container_width=True)

else:
    st.info("📌 Ajusta los parámetros en la barra lateral y presiona el botón para analizar.")
