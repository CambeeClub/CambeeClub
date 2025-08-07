import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors

# ===================== CONFIGURACIÓN INICIAL DE LA APLICACIÓN =====================
# Configura la página de Streamlit para una experiencia de usuario óptima.
# Establece el título de la pestaña del navegador, el ícono, el diseño y el estado inicial de la barra lateral.
st.set_page_config(
    page_title="Analizador de Acciones - Terminal Financiera",
    page_icon="📈",
    layout="wide",  # Utiliza todo el ancho disponible para el contenido.
    initial_sidebar_state="expanded"  # La barra lateral se muestra expandida por defecto.
)

# Aplica un tema oscuro profesional y estilos CSS personalizados para una interfaz moderna.
# Estos estilos mejoran la estética, la legibilidad y la experiencia de usuario.
st.markdown(
    """
    <style>
    /* Estilos generales para el contenedor principal de la aplicación */
    .reportview-container {
        background: #1a1a2e; /* Color de fondo principal: un azul oscuro profundo. */
        color: #e0e0e0; /* Color del texto general: un gris claro para alto contraste. */
    }
    /* Estilos para la barra lateral de Streamlit */
    .sidebar .sidebar-content {
        background: #16213e; /* Fondo de la barra lateral: ligeramente diferente al principal para distinción. */
        color: #e0e0e0; /* Color del texto en la barra lateral. */
    }
    /* Estilos para todos los títulos (h1 a h6) */
    h1, h2, h3, h4, h5, h6 {
        color: #e94560; /* Color de acento para títulos: un rojo vibrante para destacar. */
    }
    /* Estilos para los campos de entrada de texto (st.text_input, st.number_input) */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #0f3460; /* Fondo de los inputs: un azul oscuro. */
        color: #e0e0e0; /* Color del texto dentro de los inputs. */
        border: 1px solid #533483; /* Borde de inputs: un morado sutil. */
        border-radius: 0.5rem; /* Bordes redondeados para los inputs. */
        padding: 0.75rem; /* Espaciado interno. */
    }
    /* Estilos para los selectores (st.selectbox) */
    .stSelectbox>div>div {
        background-color: #0f3460; /* Fondo del selector. */
        color: #e0e0e0; /* Color del texto del selector. */
        border: 1px solid #533483; /* Borde del selector. */
        border-radius: 0.5rem; /* Bordes redondeados. */
        padding: 0.75rem; /* Espaciado interno. */
    }
    /* Estilos para los sliders (st.slider) */
    .stSlider>div>div>div>div {
        background-color: #e94560; /* Color de la barra del slider. */
    }
    /* Estilos para los botones (st.button) */
    .stButton>button {
        background-color: #e94560; /* Fondo de los botones: el color de acento rojo. */
        color: white; /* Color del texto del botón. */
        border-radius: 0.75rem; /* Bordes redondeados. */
        padding: 0.75rem 1.5rem; /* Espaciado interno. */
        transition: background-color 0.3s ease, transform 0.2s ease; /* Transiciones suaves para hover. */
    }
    /* Estilos al pasar el ratón sobre los botones */
    .stButton>button:hover {
        background-color: #b82e4a; /* Tono más oscuro al pasar el ratón. */
        transform: scale(1.02); /* Ligero aumento de tamaño para efecto interactivo. */
    }
    /* Estilos para los expanders (st.expander) */
    .stExpander {
        background-color: #16213e; /* Fondo del expander. */
        border-radius: 1rem; /* Bordes más redondeados. */
        padding: 1rem; /* Espaciado interno. */
        margin-bottom: 1rem; /* Margen inferior para separar expanders. */
        border: 1px solid #0f3460; /* Borde sutil. */
    }
    /* Estilos para el texto del título del expander */
    .stExpander div[role="button"] p {
        color: #e94560 !important; /* Color de acento para el título del expander. */
        font-weight: bold; /* Texto en negrita. */
    }
    /* Estilos para las alertas (st.info, st.warning, st.error, st.success) */
    .stAlert {
        border-radius: 0.75rem; /* Bordes redondeados para las alertas. */
    }
    /* Estilos para el texto de las pestañas (st.tabs) */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem; /* Tamaño de fuente para el texto de la pestaña. */
        color: #e0e0e0; /* Color del texto de la pestaña. */
    }
    /* Estilos para la pestaña seleccionada */
    .stTabs [data-baseweb="tab-list"] button.st-cq { /* Selector específico para la pestaña activa. */
        background-color: #e94560; /* Fondo de la pestaña activa: color de acento. */
        border-radius: 0.75rem; /* Bordes redondeados. */
        color: white; /* Color del texto. */
    }
    .stTabs [data-baseweb="tab-list"] button.st-cq p {
        color: white; /* Asegura que el texto de la pestaña activa sea blanco. */
    }
    /* Espaciado entre las pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem; /* Espacio entre las pestañas. */
    }
    /* Estilos para las pestañas no seleccionadas */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #0f3460; /* Fondo de las pestañas inactivas. */
        border-radius: 0.75rem; /* Bordes redondeados. */
        padding: 0.5rem 1rem; /* Espaciado interno. */
        color: #e0e0e0; /* Color del texto de las pestañas inactivas. */
    }
    /* Estilos para el texto de los widgets en general (ej. etiquetas de number_input) */
    .css-1d391kg {
        color: #e0e0e0; /* Asegura que las etiquetas de los widgets sean claras. */
    }
    </style>
    """,
    unsafe_allow_html=True # Permite la inyección de HTML y CSS personalizado.
)

# Inicialización de `st.session_state` para persistir los datos de entrada del usuario
# a través de las recargas de la aplicación. Esto es crucial para mantener el estado.
if 'data_inputs' not in st.session_state:
    st.session_state.data_inputs = {
        'precio_actual': 0.0,
        'eps_actual': 0.0,
        'eps_proyectado': 0.0,
        'revenue_actual': 0.0,
        'revenue_pesimista': 0.0,
        'revenue_base': 0.0,
        'revenue_optimista': 0.0,
        'net_income_estimado': 0.0,
        'acciones_circulacion': 0.0,
        'dividendos_anuales': 0.0,
        'book_value_per_share': 0.0,
        'equity_proyectado': 0.0,
        'tasa_crecimiento_esperada': 0.0,
        'wacc': 0.0,
        'per_esperado': 0.0,
        'ps_esperado': 0.0,
        'pb_esperado': 0.0,
        'margen_seguridad_deseado': 0.0,
        'años_proyeccion_dcf': 5, # Número de años por defecto para la proyección DCF.
        'tasa_crecimiento_perpetuo': 2.0, # Tasa de crecimiento perpetuo por defecto (en porcentaje).
        # Datos históricos para la comparación de múltiplos.
        'per_historico_1': 0.0,
        'per_historico_2': 0.0,
        'per_historico_3': 0.0,
        'ps_historico_1': 0.0,
        'ps_historico_2': 0.0,
        'ps_historico_3': 0.0,
        'pb_historico_1': 0.0,
        'pb_historico_2': 0.0,
        'pb_historico_3': 0.0,
    }

# ===================== FUNCIONES AUXILIARES Y DE CÁLCULO FINANCIERO =====================

# --- Validación de Inputs ---
def validar_input(valor, nombre_campo):
    """
    Valida que un valor de entrada sea un número y no sea negativo.
    Muestra un mensaje de error en Streamlit si la validación falla.
    """
    if not isinstance(valor, (int, float)):
        st.error(f"Error: '{nombre_campo}' debe ser un valor numérico.")
        return False
    if valor < 0:
        st.error(f"Error: '{nombre_campo}' debe ser un número positivo o cero.")
        return False
    return True

# --- Cálculos de Múltiplos ---
def calcular_pe(precio, eps):
    """
    Calcula el Ratio Precio/Beneficio (P/E).
    Retorna 0.0 si EPS es cero para evitar divisiones por cero.
    """
    if eps > 0:
        return precio / eps
    return 0.0

def calcular_ps(precio, revenue_per_share):
    """
    Calcula el Ratio Precio/Ventas (P/S).
    Retorna 0.0 si Revenue por Acción es cero.
    """
    if revenue_per_share > 0:
        return precio / revenue_per_share
    return 0.0

def calcular_pb(precio, book_value_per_share):
    """
    Calcula el Ratio Precio/Valor Contable (P/B).
    Retorna 0.0 si Book Value por Acción es cero.
    """
    if book_value_per_share > 0:
        return precio / book_value_per_share
    return 0.0

# ===================== SECCIÓN: Valuación por Múltiplos =====================
def valuacion_por_multiplos(data):
    """
    Realiza la valuación de la acción utilizando el método de múltiplos.
    Calcula el precio objetivo basado en los múltiplos P/E, P/S y P/B esperados.
    """
    st.subheader("Valuación por Múltiplos")
    st.markdown("Este método estima el valor de la acción comparándola con empresas similares o con sus propios múltiplos históricos/esperados.")

    precio_objetivo_pe = 0.0
    precio_objetivo_ps = 0.0
    precio_objetivo_pb = 0.0

    # Cálculo del Precio Objetivo basado en P/E Proyectado
    st.markdown("---")
    st.markdown("#### Precio Objetivo basado en P/E Proyectado")
    if data['eps_proyectado'] > 0 and data['per_esperado'] > 0:
        precio_objetivo_pe = data['eps_proyectado'] * data['per_esperado']
        st.write(f"**EPS Proyectado:** ${data['eps_proyectado']:,.2f}")
        st.write(f"**PER Esperado:** {data['per_esperado']:,.2f}x")
        st.success(f"**Precio Objetivo (P/E Proyectado):** ${precio_objetivo_pe:,.2f}")
    else:
        st.warning("No se puede calcular el Precio Objetivo (P/E Proyectado). Asegúrate de ingresar EPS Proyectado y PER Esperado > 0.")

    # Cálculo del Precio Objetivo basado en P/S Proyectado
    st.markdown("---")
    st.markdown("#### Precio Objetivo basado en P/S Proyectado")
    revenue_proyectado_base = data['revenue_base']
    if data['acciones_circulacion'] > 0 and revenue_proyectado_base > 0 and data['ps_esperado'] > 0:
        revenue_per_share_proyectado = revenue_proyectado_base / data['acciones_circulacion']
        precio_objetivo_ps = revenue_per_share_proyectado * data['ps_esperado']
        st.write(f"**Revenue Proyectado (Base):** ${revenue_proyectado_base:,.2f}")
        st.write(f"**Acciones en Circulación:** {data['acciones_circulacion']:,.0f}")
        st.write(f"**Revenue por Acción Proyectado:** ${revenue_per_share_proyectado:,.2f}")
        st.write(f"**P/S Esperado:** {data['ps_esperado']:,.2f}x")
        st.success(f"**Precio Objetivo (P/S Proyectado):** ${precio_objetivo_ps:,.2f}")
    else:
        st.warning("No se puede calcular el Precio Objetivo (P/S Proyectado). Asegúrate de ingresar Revenue Base, Acciones en Circulación y P/S Esperado > 0.")

    # Cálculo del Precio Objetivo basado en P/B Proyectado
    st.markdown("---")
    st.markdown("#### Precio Objetivo basado en P/B Proyectado")
    if data['equity_proyectado'] > 0 and data['acciones_circulacion'] > 0 and data['pb_esperado'] > 0:
        book_value_per_share_proyectado = data['equity_proyectado'] / data['acciones_circulacion']
        precio_objetivo_pb = book_value_per_share_proyectado * data['pb_esperado']
        st.write(f"**Equity Proyectado:** ${data['equity_proyectado']:,.2f}")
        st.write(f"**Acciones en Circulación:** {data['acciones_circulacion']:,.0f}")
        st.write(f"**Book Value por Acción Proyectado:** ${book_value_per_share_proyectado:,.2f}")
        st.write(f"**P/B Esperado:** {data['pb_esperado']:,.2f}x")
        st.success(f"**Precio Objetivo (P/B Proyectado):** ${precio_objetivo_pb:,.2f}")
    else:
        st.warning("No se puede calcular el Precio Objetivo (P/B Proyectado). Asegúrate de ingresar Equity Proyectado, Acciones en Circulación y P/B Esperado > 0.")

    # Promedio simple de precios objetivo por múltiplos válidos
    st.markdown("---")
    precios_validos = [p for p in [precio_objetivo_pe, precio_objetivo_ps, precio_objetivo_pb] if p > 0]
    if precios_validos:
        precio_promedio_multiplos = np.mean(precios_validos)
        st.success(f"**Precio Objetivo Promedio por Múltiplos:** ${precio_promedio_multiplos:,.2f}")
        return precio_promedio_multiplos
    else:
        st.info("No se pudo calcular un precio objetivo promedio por múltiplos. Se necesitan más datos válidos.")
        return 0.0

# ===================== SECCIÓN: Descuento de Flujos de Caja (DCF) =====================
def valuacion_dcf(data, nombre_escenario="Base", factor_crecimiento=1.0, factor_wacc=1.0):
    """
    Realiza la valuación de la acción utilizando el método de Descuento de Flujos de Caja (DCF).
    Proyecta el Flujo de Caja Libre (FCF) y lo descuenta al presente.
    Ajusta la tasa de crecimiento y WACC según el factor del escenario.
    """
    st.subheader(f"Valuación DCF - Escenario {nombre_escenario}")
    st.markdown("El DCF estima el valor intrínseco de una empresa basándose en sus flujos de caja futuros proyectados, descontados a su valor presente.")

    # Parámetros clave para DCF, ajustados por el factor del escenario
    net_income_estimado = data['net_income_estimado']
    acciones_circulacion = data['acciones_circulacion']
    wacc = (data['wacc'] / 100) * factor_wacc # Ajuste del WACC por escenario
    tasa_crecimiento_esperada = (data['tasa_crecimiento_esperada'] / 100) * factor_crecimiento # Ajuste de tasa de crecimiento
    años_proyeccion = int(data['años_proyeccion_dcf'])
    tasa_crecimiento_perpetuo = (data['tasa_crecimiento_perpetuo'] / 100) # La tasa perpetua no se ajusta por escenario

    # Validación de parámetros mínimos
    if not all([net_income_estimado > 0, acciones_circulacion > 0, wacc > 0, tasa_crecimiento_esperada >= 0, años_proyeccion > 0]):
        st.warning(f"No se puede realizar la valuación DCF para el escenario {nombre_escenario}. Faltan datos clave (Net Income Estimado, Acciones en Circulación, WACC, Tasa de Crecimiento Esperada, Años de Proyección).")
        return 0.0, []

    st.write(f"**Parámetros DCF para {nombre_escenario}:**")
    st.write(f"- Años de Proyección Explícita: {años_proyeccion}")
    st.write(f"- WACC (Tasa de Descuento Ajustada): {wacc*100:.2f}%")
    st.write(f"- Tasa de Crecimiento Esperada (Fase 1 Ajustada): {tasa_crecimiento_esperada*100:.2f}%")
    st.write(f"- Tasa de Crecimiento Perpetuo (Fase 2): {tasa_crecimiento_perpetuo*100:.2f}%")
    st.write(f"- Net Income Estimado Inicial: ${net_income_estimado:,.2f}")

    # Proyección de Flujos de Caja Libres (FCF)
    # Simplificación: Asumimos FCF = Net Income para este modelo sin APIs.
    # En un modelo real, el FCF se calcularía con más detalle.
    fcf_proyectados = []
    valor_presente_fcf = 0.0
    
    st.markdown("---")
    st.write("**Proyección de Flujos de Caja Libres (FCF) y su Valor Presente:**")
    st.write("*(Asumiendo FCF = Net Income para simplificación)*")

    current_fcf = net_income_estimado # FCF del Año 0 (base para la proyección)
    
    # Tabla para mostrar la proyección de FCF
    fcf_table_data = [["Año", "FCF Proyectado", "Factor de Descuento", "Valor Presente FCF"]]

    for i in range(1, años_proyeccion + 1):
        # El FCF crece a la tasa de crecimiento esperada
        current_fcf *= (1 + tasa_crecimiento_esperada)
        fcf_proyectados.append(current_fcf)
        
        # Descontamos el FCF al valor presente usando el WACC
        factor_descuento = (1 + wacc)**i
        vp_fcf_año = current_fcf / factor_descuento
        valor_presente_fcf += vp_fcf_año
        fcf_table_data.append([f"{i}", f"${current_fcf:,.2f}", f"1/({factor_descuento:,.2f})", f"${vp_fcf_año:,.2f}"])
    
    st.table(pd.DataFrame(fcf_table_data[1:], columns=fcf_table_data[0]))
    st.write(f"**Suma Total de Valores Presentes de FCF (Fase 1 - Período Explícito):** ${valor_presente_fcf:,.2f}")

    # ===================== Método de Crecimiento Perpetuo (parte del DCF) =====================
    st.markdown("---")
    st.write("**Cálculo de Valor Terminal (Método de Crecimiento Perpetuo):**")
    st.markdown("El Valor Terminal representa el valor de todos los flujos de caja futuros de la empresa más allá del período de proyección explícita.")
    
    valor_terminal = 0.0
    if wacc > tasa_crecimiento_perpetuo:
        # El FCF del último año proyectado es la base para el cálculo del valor terminal.
        fcf_ultimo_año_proyeccion = fcf_proyectados[-1] if fcf_proyectados else net_income_estimado
        # El FCF para el primer año de la perpetuidad (Año N+1)
        fcf_siguiente_periodo = fcf_ultimo_año_proyeccion * (1 + tasa_crecimiento_perpetuo)
        
        # Fórmula de crecimiento perpetuo (Gordon Growth Model)
        valor_terminal = fcf_siguiente_periodo / (wacc - tasa_crecimiento_perpetuo)
        
        st.write(f"FCF del Último Año Proyectado (Año {años_proyeccion}): ${fcf_ultimo_año_proyeccion:,.2f}")
        st.write(f"FCF del Siguiente Periodo (Año {años_proyeccion + 1} para Perpetuidad): ${fcf_siguiente_periodo:,.2f}")
        st.write(f"**Valor Terminal (al final del Año {años_proyeccion}):** ${valor_terminal:,.2f}")
    else:
        st.warning("Advertencia: Para calcular el Valor Terminal por crecimiento perpetuo, el WACC debe ser mayor que la Tasa de Crecimiento Perpetuo.")

    # Valor Presente del Valor Terminal
    valor_presente_valor_terminal = valor_terminal / ((1 + wacc)**años_proyeccion)
    st.write(f"**Valor Presente del Valor Terminal:** ${valor_presente_valor_terminal:,.2f}")

    # Valor de la Empresa (Enterprise Value)
    valor_empresa = valor_presente_fcf + valor_presente_valor_terminal
    st.write(f"**Valor Total de la Empresa (Suma de FCF Descontados + Valor Terminal Descontado):** ${valor_empresa:,.2f}")

    # Valor de la Equidad (Equity Value)
    # Para este modelo simplificado, asumimos que el Valor de la Equidad es igual al Valor de la Empresa.
    # En un análisis real, se ajustaría por la deuda neta y el efectivo.
    valor_equidad = valor_empresa 
    st.write(f"**Valor de la Equidad (Implícito):** ${valor_equidad:,.2f}")

    # Precio Objetivo por Acción
    precio_objetivo_dcf = 0.0
    if acciones_circulacion > 0:
        precio_objetivo_dcf = valor_equidad / acciones_circulacion
        st.success(f"**Precio Objetivo por Acción (DCF - {nombre_escenario}):** ${precio_objetivo_dcf:,.2f}")
    else:
        st.warning("No se puede calcular el Precio Objetivo por Acción. El número de acciones en circulación es cero.")
    
    return precio_objetivo_dcf, fcf_proyectados

# ===================== Método de Múltiplo Terminal (Exit Multiple) =====================
def valuacion_multiplo_terminal(data, nombre_escenario="Base", factor_crecimiento=1.0, factor_wacc=1.0):
    """
    Realiza la valuación utilizando el método de Múltiplo Terminal (Exit Multiple).
    Calcula el valor terminal aplicando un múltiplo (ej. P/E) a una métrica financiera proyectada
    al final del período de proyección.
    """
    st.subheader(f"Valuación por Múltiplo Terminal - Escenario {nombre_escenario}")
    st.markdown("Este método estima el valor de la empresa al final del período de proyección explícita, aplicando un múltiplo de valoración a una métrica financiera clave.")

    # Parámetros clave, ajustados por el factor del escenario
    net_income_estimado = data['net_income_estimado']
    acciones_circulacion = data['acciones_circulacion']
    wacc = (data['wacc'] / 100) * factor_wacc
    tasa_crecimiento_esperada = (data['tasa_crecimiento_esperada'] / 100) * factor_crecimiento
    años_proyeccion = int(data['años_proyeccion_dcf'])
    per_terminal_esperado = data['per_esperado'] # Usamos el PER esperado como múltiplo terminal

    # Validación de parámetros mínimos
    if not all([net_income_estimado > 0, acciones_circulacion > 0, wacc > 0, tasa_crecimiento_esperada >= 0, años_proyeccion > 0, per_terminal_esperado > 0]):
        st.warning(f"No se puede realizar la valuación por Múltiplo Terminal para el escenario {nombre_escenario}. Faltan datos clave (Net Income Estimado, Acciones en Circulación, WACC, Tasa de Crecimiento Esperada, Años de Proyección, PER Esperado).")
        return 0.0

    st.write(f"**Parámetros Múltiplo Terminal para {nombre_escenario}:**")
    st.write(f"- Años de Proyección Explícita: {años_proyeccion}")
    st.write(f"- WACC (Tasa de Descuento Ajustada): {wacc*100:.2f}%")
    st.write(f"- Tasa de Crecimiento Esperada (Ajustada): {tasa_crecimiento_esperada*100:.2f}%")
    st.write(f"- PER Terminal Esperado: {per_terminal_esperado:.2f}x")

    # Proyección de Net Income hasta el último año del período explícito
    net_income_proyectado_final = net_income_estimado
    for i in range(años_proyeccion):
        net_income_proyectado_final *= (1 + tasa_crecimiento_esperada)
    
    st.write(f"Net Income Proyectado al final del Año {años_proyeccion}: ${net_income_proyectado_final:,.2f}")

    # Cálculo del Valor Terminal aplicando el múltiplo PER al Net Income proyectado
    valor_terminal_multiplo = net_income_proyectado_final * per_terminal_esperado
    st.write(f"**Valor Terminal (al final del Año {años_proyeccion}):** ${valor_terminal_multiplo:,.2f}")

    # Descontar el Valor Terminal al presente
    valor_presente_multiplo_terminal = valor_terminal_multiplo / ((1 + wacc)**años_proyeccion)
    st.write(f"**Valor Presente del Valor Terminal:** ${valor_presente_multiplo_terminal:,.2f}")

    # El precio objetivo se basa en el valor presente del valor terminal
    precio_objetivo_multiplo_terminal = 0.0
    if acciones_circulacion > 0:
        precio_objetivo_multiplo_terminal = valor_presente_multiplo_terminal / acciones_circulacion
        st.success(f"**Precio Objetivo por Acción (Múltiplo Terminal - {nombre_escenario}):** ${precio_objetivo_multiplo_terminal:,.2f}")
    else:
        st.warning("No se puede calcular el Precio Objetivo por Acción. El número de acciones en circulación es cero.")

    return precio_objetivo_multiplo_terminal

# ===================== SECCIÓN: Generación de Reporte PDF =====================
def generar_reporte_pdf(data, resultados):
    """
    Genera un reporte PDF completo con los resultados del análisis de acciones.
    Utiliza la librería ReportLab para crear un documento estructurado y profesional.
    """
    doc = SimpleDocTemplate("analisis_acciones_reporte.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Definición de estilos personalizados para el PDF para una mejor presentación.
    styles.add(ParagraphStyle(name='TitleStyle', fontSize=24, leading=28, alignment=TA_CENTER,
                              fontName='Helvetica-Bold', textColor=colors.HexColor('#e94560')))
    styles.add(ParagraphStyle(name='SubtitleStyle', fontSize=16, leading=20, alignment=TA_CENTER,
                              fontName='Helvetica-Bold', textColor=colors.HexColor('#533483')))
    styles.add(ParagraphStyle(name='Heading1Style', fontSize=18, leading=22, alignment=TA_LEFT,
                              fontName='Helvetica-Bold', textColor=colors.HexColor('#0f3460')))
    styles.add(ParagraphStyle(name='Heading2Style', fontSize=14, leading=18, alignment=TA_LEFT,
                              fontName='Helvetica-Bold', textColor=colors.HexColor('#e94560')))
    styles.add(ParagraphStyle(name='NormalStyle', fontSize=10, leading=12, alignment=TA_LEFT,
                              fontName='Helvetica', textColor=colors.black))
    styles.add(ParagraphStyle(name='BoldStyle', fontSize=10, leading=12, alignment=TA_LEFT,
                              fontName='Helvetica-Bold', textColor=colors.black))
    styles.add(ParagraphStyle(name='CenterNormalStyle', fontSize=10, leading=12, alignment=TA_CENTER,
                              fontName='Helvetica', textColor=colors.black))
    styles.add(ParagraphStyle(name='DisclaimerStyle', fontSize=8, leading=10, alignment=TA_CENTER,
                              fontName='Helvetica-Oblique', textColor=colors.grey))

    story = [] # Lista para almacenar los elementos del documento PDF.

    # Sección de Título y Subtítulo del Reporte
    story.append(Paragraph("Reporte de Análisis de Acciones", styles['TitleStyle']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Simulador de Terminal Financiera", styles['SubtitleStyle']))
    story.append(Spacer(1, 0.5 * inch))

    # Sección de Introducción y Descargo de Responsabilidad (Disclaimer)
    story.append(Paragraph("Este reporte presenta un análisis financiero de acciones basado en datos ingresados manualmente por el usuario. Es una simulación y no debe considerarse como asesoramiento de inversión profesional. Los resultados dependen enteramente de la precisión y las suposiciones de los datos proporcionados.", styles['NormalStyle']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Descargo de Responsabilidad: Este documento es solo para fines educativos y de simulación. No constituye una recomendación para comprar o vender ningún valor. Siempre consulte a un profesional financiero calificado antes de tomar decisiones de inversión.", styles['DisclaimerStyle']))
    story.append(Spacer(1, 0.5 * inch))
    story.append(PageBreak()) # Salto de página para una mejor organización.

    # Sección de Datos Ingresados por el Usuario
    story.append(Paragraph("1. Datos Ingresados por el Usuario", styles['Heading1Style']))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Aquí se resumen todos los datos fundamentales y de proyección que fueron proporcionados para el análisis.", styles['NormalStyle']))
    story.append(Spacer(1, 0.1 * inch))
    
    # Datos fundamentales
    data_table_data_fundamentales = [
        ["Métrica", "Valor"],
        ["Precio Actual", f"${data['precio_actual']:,.2f}"],
        ["EPS Actual", f"${data['eps_actual']:,.2f}"],
        ["EPS Proyectado", f"${data['eps_proyectado']:,.2f}"],
        ["Revenue Actual", f"${data['revenue_actual']:,.2f}"],
        ["Net Income Estimado", f"${data['net_income_estimado']:,.2f}"],
        ["Acciones en Circulación", f"{data['acciones_circulacion']:,.0f}"],
        ["Dividendos Anuales", f"${data['dividendos_anuales']:,.2f}"],
        ["Book Value per Share", f"${data['book_value_per_share']:,.2f}"],
        ["Equity Proyectado", f"${data['equity_proyectado']:,.2f}"],
    ]

    # Proyecciones y tasas
    data_table_data_proyecciones = [
        ["Métrica", "Valor"],
        ["Tasa de Crecimiento Esperada", f"{data['tasa_crecimiento_esperada']:.2f}%"],
        ["WACC / Tasa de Descuento", f"{data['wacc']:.2f}%"],
        ["Margen de Seguridad Deseado", f"{data['margen_seguridad_deseado']:.2f}%"],
        ["Años de Proyección DCF", f"{data['años_proyeccion_dcf']}"],
        ["Tasa Crecimiento Perpetuo", f"{data['tasa_crecimiento_perpetuo']:.2f}%"],
    ]

    # Múltiplos esperados
    data_table_data_multiplos_esperados = [
        ["Métrica", "Valor"],
        ["PER Esperado", f"{data['per_esperado']:.2f}x"],
        ["P/S Esperado", f"{data['ps_esperado']:.2f}x"],
        ["P/B Esperado", f"{data['pb_esperado']:.2f}x"],
    ]

    # Múltiplos históricos
    data_table_data_multiplos_historicos = [
        ["Métrica", "Año -2", "Año -1", "Actual"],
        ["PER Histórico", f"{data['per_historico_1']:.2f}x", f"{data['per_historico_2']:.2f}x", f"{data['per_historico_3']:.2f}x"],
        ["P/S Histórico", f"{data['ps_historico_1']:.2f}x", f"{data['ps_historico_2']:.2f}x", f"{data['ps_historico_3']:.2f}x"],
        ["P/B Histórico", f"{data['pb_historico_1']:.2f}x", f"{data['pb_historico_2']:.2f}x", f"{data['pb_historico_3']:.2f}x"],
    ]

    # Escenarios de Revenue
    data_table_data_revenue_escenarios = [
        ["Métrica", "Valor"],
        ["Revenue Estimado (Pesimista)", f"${data['revenue_pesimista']:,.2f}"],
        ["Revenue Estimado (Base)", f"${data['revenue_base']:,.2f}"],
        ["Revenue Estimado (Optimista)", f"${data['revenue_optimista']:,.2f}"],
    ]
    
    # Estilo general para las tablas de datos
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e94560')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f4f8')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ])
    
    story.append(Paragraph("Datos Fundamentales:", styles['BoldStyle']))
    t_fundamentales = Table(data_table_data_fundamentales)
    t_fundamentales.setStyle(table_style)
    story.append(t_fundamentales)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Proyecciones y Tasas de Descuento:", styles['BoldStyle']))
    t_proyecciones = Table(data_table_data_proyecciones)
    t_proyecciones.setStyle(table_style)
    story.append(t_proyecciones)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Múltiplos Esperados:", styles['BoldStyle']))
    t_multiplos_esperados = Table(data_table_data_multiplos_esperados)
    t_multiplos_esperados.setStyle(table_style)
    story.append(t_multiplos_esperados)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Múltiplos Históricos (para referencia):", styles['BoldStyle']))
    t_multiplos_historicos = Table(data_table_data_multiplos_historicos)
    t_multiplos_historicos.setStyle(table_style)
    story.append(t_multiplos_historicos)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Escenarios de Revenue Estimado:", styles['BoldStyle']))
    t_revenue_escenarios = Table(data_table_data_revenue_escenarios)
    t_revenue_escenarios.setStyle(table_style)
    story.append(t_revenue_escenarios)
    story.append(Spacer(1, 0.5 * inch))
    story.append(PageBreak())

    # Sección de Análisis de Múltiplos
    story.append(Paragraph("2. Análisis de Múltiplos", styles['Heading1Style']))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Esta sección presenta los múltiplos de valoración actuales y proyectados, junto con una interpretación de su relación con los múltiplos esperados e históricos.", styles['NormalStyle']))
    story.append(Spacer(1, 0.1 * inch))

    multiplos_calculados_data = [
        ["Métrica", "Actual", "Proyectado"],
        ["P/E (x)", f"{resultados['pe_actual']:.2f}", f"{resultados['pe_proyectado']:.2f}"],
        ["P/S (x)", f"{resultados['ps_actual']:.2f}", f"{resultados['ps_proyectado']:.2f}"],
        ["P/B (x)", f"{resultados['pb_actual']:.2f}", f"{resultados['pb_proyectado']:.2f}"],
    ]
    t_multiplos_calculados = Table(multiplos_calculados_data)
    t_multiplos_calculados.setStyle(table_style)
    story.append(t_multiplos_calculados)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Interpretación de Múltiplos:", styles['Heading2Style']))
    for rec in resultados['recomendaciones_multiplos']:
        story.append(Paragraph(f"- {rec}", styles['NormalStyle']))
        story.append(Spacer(1, 0.05 * inch))
    story.append(Spacer(1, 0.5 * inch))
    story.append(PageBreak())

    # Sección de Valuación por Escenarios
    story.append(Paragraph("3. Valuación por Escenarios", styles['Heading1Style']))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Se presenta la valuación de la acción bajo diferentes escenarios (pesimista, base, optimista) utilizando el método de Descuento de Flujos de Caja (DCF) y Múltiplo Terminal.", styles['NormalStyle']))
    story.append(Spacer(1, 0.1 * inch))

    escenarios_valuacion_data = [
        ["Escenario", "Precio Objetivo DCF", "Precio Objetivo Múltiplo Terminal"],
        ["Pesimista", f"${resultados['precio_obj_dcf_pesimista']:,.2f}", f"${resultados['precio_obj_multiplo_terminal_pesimista']:,.2f}"],
        ["Base", f"${resultados['precio_obj_dcf_base']:,.2f}", f"${resultados['precio_obj_multiplo_terminal_base']:,.2f}"],
        ["Optimista", f"${resultados['precio_obj_dcf_optimista']:,.2f}", f"${resultados['precio_obj_multiplo_terminal_optimista']:,.2f}"],
    ]
    t_escenarios_valuacion = Table(escenarios_valuacion_data)
    t_escenarios_valuacion.setStyle(table_style)
    story.append(t_escenarios_valuacion)
    story.append(Spacer(1, 0.2 * inch))

    if resultados['fcf_proyectados_base']:
        story.append(Paragraph("Proyección de Flujos de Caja Libres (FCF) - Escenario Base:", styles['Heading2Style']))
        fcf_data_pdf = [["Año", "FCF Proyectado ($)"]]
        for i, fcf in enumerate(resultados['fcf_proyectados_base']):
            fcf_data_pdf.append([f"Año {i+1}", f"{fcf:,.2f}"])
        
        t_fcf_pdf = Table(fcf_data_pdf)
        t_fcf_pdf.setStyle(table_style)
        story.append(t_fcf_pdf)
        story.append(Spacer(1, 0.5 * inch))
    story.append(PageBreak())

    # Sección de Resumen de Valuación y Recomendaciones
    story.append(Paragraph("4. Resumen de Valuación y Recomendaciones", styles['Heading1Style']))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Esta sección consolida los resultados de los diferentes métodos de valuación y proporciona recomendaciones finales basadas en el análisis.", styles['NormalStyle']))
    story.append(Spacer(1, 0.1 * inch))

    final_results_data = [
        ["Métrica", "Valor"],
        ["Precio Objetivo Promedio por Múltiplos", f"${resultados['precio_obj_multiplos']:,.2f}"],
        ["Precio Justo Final (Promedio Ponderado)", f"${resultados['precio_justo_final']:,.2f}"],
        ["Precio Máximo a Pagar (con Margen de Seguridad)", f"${resultados['precio_maximo_a_pagar']:,.2f}"],
    ]
    t_final_results = Table(final_results_data)
    t_final_results.setStyle(table_style)
    story.append(t_final_results)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Recomendaciones Generales:", styles['Heading2Style']))
    for rec in resultados['recomendaciones_generales']:
        story.append(Paragraph(f"- {rec}", styles['NormalStyle']))
        story.append(Spacer(1, 0.05 * inch))
    story.append(Spacer(1, 0.5 * inch))

    # Construir el PDF
    try:
        doc.build(story)
        st.success("Reporte PDF generado exitosamente: `analisis_acciones_reporte.pdf`")
        with open("analisis_acciones_reporte.pdf", "rb") as file:
            st.download_button(
                label="Descargar Reporte PDF",
                data=file,
                file_name="analisis_acciones_reporte.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"Error al generar el PDF: {e}")

# ===================== SECCIÓN: Guardar y Cargar Datos =====================
def guardar_datos_locales():
    """
    Guarda los datos de la sesión actual (inputs del usuario) en un archivo JSON local.
    Esto permite al usuario guardar su progreso y cargarlo más tarde.
    """
    try:
        with open("analisis_acciones_data.json", "w") as f:
            json.dump(st.session_state.data_inputs, f, indent=4) # Guarda con formato legible.
        st.success("Datos guardados exitosamente en `analisis_acciones_data.json`")
    except Exception as e:
        st.error(f"Error al guardar los datos: {e}")

def cargar_datos_locales():
    """
    Carga los datos desde un archivo JSON local a la sesión actual de Streamlit.
    Recarga la aplicación para que los nuevos datos se reflejen en la interfaz.
    """
    try:
        with open("analisis_acciones_data.json", "r") as f:
            loaded_data = json.load(f)
            # Actualiza solo las claves existentes para evitar errores si el archivo JSON es antiguo.
            for key, value in loaded_data.items():
                if key in st.session_state.data_inputs:
                    st.session_state.data_inputs[key] = value
        st.success("Datos cargados exitosamente desde `analisis_acciones_data.json`")
        st.experimental_rerun() # Fuerza una recarga de la aplicación para actualizar la UI.
    except FileNotFoundError:
        st.warning("No se encontró el archivo `analisis_acciones_data.json`. Por favor, guarda datos primero.")
    except json.JSONDecodeError:
        st.error("Error al decodificar el archivo JSON. Asegúrate de que el formato sea correcto.")
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")

def reiniciar_datos():
    """
    Reinicia todos los datos de la sesión a sus valores por defecto.
    Esto limpia todos los inputs y cálculos previos.
    """
    st.session_state.data_inputs = {
        'precio_actual': 0.0,
        'eps_actual': 0.0,
        'eps_proyectado': 0.0,
        'revenue_actual': 0.0,
        'revenue_pesimista': 0.0,
        'revenue_base': 0.0,
        'revenue_optimista': 0.0,
        'net_income_estimado': 0.0,
        'acciones_circulacion': 0.0,
        'dividendos_anuales': 0.0,
        'book_value_per_share': 0.0,
        'equity_proyectado': 0.0,
        'tasa_crecimiento_esperada': 0.0,
        'wacc': 0.0,
        'per_esperado': 0.0,
        'ps_esperado': 0.0,
        'pb_esperado': 0.0,
        'margen_seguridad_deseado': 0.0,
        'años_proyeccion_dcf': 5,
        'tasa_crecimiento_perpetuo': 2.0, # En porcentaje
        'per_historico_1': 0.0,
        'per_historico_2': 0.0,
        'per_historico_3': 0.0,
        'ps_historico_1': 0.0,
        'ps_historico_2': 0.0,
        'ps_historico_3': 0.0,
        'pb_historico_1': 0.0,
        'pb_historico_2': 0.0,
        'pb_historico_3': 0.0,
    }
    st.experimental_rerun() # Fuerza una recarga de la aplicación para reflejar los datos reiniciados.

# ===================== BARRA LATERAL (SIDEBAR) DE NAVEGACIÓN Y UTILIDADES =====================
with st.sidebar:
    # Logo ficticio para dar un toque profesional a la interfaz.
    st.image("https://placehold.co/150x50/e94560/ffffff?text=FINTECH+LOGO", use_column_width=True) 
    st.title("Menú de Navegación")
    st.markdown("---") # Separador visual.
    
    st.subheader("Gestión de Datos")
    # Columnas para organizar los botones de guardar y cargar.
    col_save, col_load = st.columns(2)
    with col_save:
        if st.button("💾 Guardar Datos", help="Guarda los datos de entrada actuales en un archivo JSON."):
            guardar_datos_locales()
    with col_load:
        if st.button("📂 Cargar Datos", help="Carga los datos de entrada desde un archivo JSON guardado previamente."):
            cargar_datos_locales()
    
    # Botón para reiniciar todos los datos a sus valores por defecto.
    if st.button("🔄 Reiniciar Datos", help="Borra todos los datos ingresados y los valores calculados, restaurando la aplicación a su estado inicial."):
        reiniciar_datos()
    
    st.markdown("---") # Separador visual.
    st.info("¡Bienvenido al Analizador de Acciones! Ingresa tus datos en la sección principal para empezar el análisis financiero detallado.")

# ===================== INTERFAZ PRINCIPAL DE LA APLICACIÓN =====================
st.title("📈 Analizador de Acciones: Terminal Financiera")
st.markdown("Una herramienta de análisis de acciones tipo **Bloomberg Terminal**, pero completamente **sin APIs ni internet**. Todos los datos son ingresados manualmente por ti. ¡Ideal para practicar y simular análisis de valuación!")

# ===================== SECCIÓN: 1. ENTRADA DE DATOS =====================
st.header("1. Entrada de Datos Financieros")
st.markdown("---") # Separador visual para la sección.

# Expander para organizar los datos fundamentales de la acción.
with st.expander("📊 Datos Fundamentales de la Acción", expanded=True):
    col1, col2 = st.columns(2) # Dos columnas para una mejor distribución de inputs.
    with col1:
        st.session_state.data_inputs['precio_actual'] = st.number_input(
            "Precio Actual de la Acción ($)",
            min_value=0.0, value=st.session_state.data_inputs['precio_actual'], format="%.2f",
            help="El precio de mercado actual de una acción de la empresa."
        )
        st.session_state.data_inputs['eps_actual'] = st.number_input(
            "EPS Actual ($)",
            min_value=0.0, value=st.session_state.data_inputs['eps_actual'], format="%.2f",
            help="Ganancia por Acción (Earnings Per Share) actual de la empresa. Representa la porción de las ganancias de una empresa asignada a cada acción común en circulación."
        )
        st.session_state.data_inputs['eps_proyectado'] = st.number_input(
            "EPS Proyectado ($)",
            min_value=0.0, value=st.session_state.data_inputs['eps_proyectado'], format="%.2f",
            help="Ganancia por Acción (Earnings Per Share) proyectado para el próximo período fiscal. Es una estimación del rendimiento futuro."
        )
        st.session_state.data_inputs['acciones_circulacion'] = st.number_input(
            "Número de Acciones en Circulación",
            min_value=0.0, value=st.session_state.data_inputs['acciones_circulacion'], format="%.0f",
            help="El número total de acciones comunes de una empresa que están actualmente en manos de los inversores."
        )
    with col2:
        st.session_state.data_inputs['revenue_actual'] = st.number_input(
            "Revenue Actual ($)",
            min_value=0.0, value=st.session_state.data_inputs['revenue_actual'], format="%.2f",
            help="Los ingresos totales (Revenue) actuales generados por la empresa a partir de sus operaciones principales."
        )
        st.session_state.data_inputs['net_income_estimado'] = st.number_input(
            "Net Income Estimado ($)",
            min_value=0.0, value=st.session_state.data_inputs['net_income_estimado'], format="%.2f",
            help="La ganancia neta (Net Income) estimada para el próximo período fiscal. Es la cantidad de dinero que queda después de restar todos los gastos e impuestos de los ingresos."
        )
        st.session_state.data_inputs['dividendos_anuales'] = st.number_input(
            "Dividendos Anuales Esperados ($)",
            min_value=0.0, value=st.session_state.data_inputs['dividendos_anuales'], format="%.2f",
            help="La cantidad total de dividendos por acción que se espera que la empresa pague anualmente a sus accionistas."
        )
        st.session_state.data_inputs['book_value_per_share'] = st.number_input(
            "Valor Contable por Acción (Book Value per Share) ($)",
            min_value=0.0, value=st.session_state.data_inputs['book_value_per_share'], format="%.2f",
            help="El valor contable de los activos de la empresa por cada acción en circulación. Se calcula como (Activos Totales - Pasivos Totales) / Acciones en Circulación."
        )
        st.session_state.data_inputs['equity_proyectado'] = st.number_input(
            "Equity Proyectado ($)",
            min_value=0.0, value=st.session_state.data_inputs['equity_proyectado'], format="%.2f",
            help="El valor total del patrimonio (Equity) proyectado de la empresa para un período futuro. Representa el valor residual de los activos después de deducir los pasivos."
        )

# Expander para organizar las proyecciones y tasas de descuento.
with st.expander("📈 Proyecciones y Tasas de Descuento", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.data_inputs['tasa_crecimiento_esperada'] = st.number_input(
            "Tasa de Crecimiento Esperada (%)",
            min_value=0.0, max_value=100.0, value=st.session_state.data_inputs['tasa_crecimiento_esperada'], format="%.2f",
            help="La tasa de crecimiento anual esperada para las ganancias, ingresos o flujos de caja de la empresa durante el período de proyección explícita."
        )
        st.session_state.data_inputs['wacc'] = st.number_input(
            "WACC / Tasa de Descuento (%)",
            min_value=0.0, max_value=100.0, value=st.session_state.data_inputs['wacc'], format="%.2f",
            help="El Costo Promedio Ponderado del Capital (Weighted Average Cost of Capital - WACC) o la tasa de descuento utilizada para traer los flujos de caja futuros a valor presente. Representa el costo de financiar los activos de la empresa."
        )
        st.session_state.data_inputs['margen_seguridad_deseado'] = st.number_input(
            "Margen de Seguridad Deseado (%)",
            min_value=0.0, max_value=100.0, value=st.session_state.data_inputs['margen_seguridad_deseado'], format="%.2f",
            help="El porcentaje de descuento sobre el precio justo que un inversor desea como colchón de seguridad. Un margen de seguridad protege contra errores en la valuación y la volatilidad del mercado."
        )
    with col2:
        st.session_state.data_inputs['años_proyeccion_dcf'] = st.slider(
            "Años de Proyección para DCF",
            min_value=1, max_value=10, value=st.session_state.data_inputs['años_proyeccion_dcf'],
            help="El número de años para los cuales se proyectan explícitamente los flujos de caja en el modelo de Descuento de Flujos de Caja (DCF)."
        )
        st.session_state.data_inputs['tasa_crecimiento_perpetuo'] = st.number_input(
            "Tasa de Crecimiento Perpetuo (%)",
            min_value=0.0, max_value=10.0, value=st.session_state.data_inputs['tasa_crecimiento_perpetuo'], format="%.2f",
            help="La tasa de crecimiento asumida para los flujos de caja de la empresa después del período de proyección explícita, en el modelo de crecimiento perpetuo del DCF."
        )

# Expander para organizar los múltiplos esperados e históricos.
with st.expander("📊 Múltiplos Esperados y Históricos", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Múltiplos Esperados (para Valuación)")
        st.session_state.data_inputs['per_esperado'] = st.number_input(
            "PER Esperado (x)",
            min_value=0.0, value=st.session_state.data_inputs['per_esperado'], format="%.2f",
            help="El Ratio Precio/Beneficio (P/E) que se espera que la acción alcance o que se considera justo para la valuación."
        )
        st.session_state.data_inputs['ps_esperado'] = st.number_input(
            "P/S Esperado (x)",
            min_value=0.0, value=st.session_state.data_inputs['ps_esperado'], format="%.2f",
            help="El Ratio Precio/Ventas (P/S) que se espera o se considera justo para la valuación."
        )
        st.session_state.data_inputs['pb_esperado'] = st.number_input(
            "P/B Esperado (x)",
            min_value=0.0, value=st.session_state.data_inputs['pb_esperado'], format="%.2f",
            help="El Ratio Precio/Valor Contable (P/B) que se espera o se considera justo para la valuación."
        )
    with col2:
        st.markdown("#### Múltiplos Históricos (Para Comparación)")
        st.markdown("Ingresa datos históricos para comparar con los múltiplos actuales y proyectados.")
        st.session_state.data_inputs['per_historico_1'] = st.number_input("PER Histórico Año -2 (x)", min_value=0.0, value=st.session_state.data_inputs['per_historico_1'], format="%.2f", help="PER de hace dos años.")
        st.session_state.data_inputs['per_historico_2'] = st.number_input("PER Histórico Año -1 (x)", min_value=0.0, value=st.session_state.data_inputs['per_historico_2'], format="%.2f", help="PER del año pasado.")
        st.session_state.data_inputs['per_historico_3'] = st.number_input("PER Histórico Año Actual (x)", min_value=0.0, value=st.session_state.data_inputs['per_historico_3'], format="%.2f", help="PER del año actual.")
        
        st.session_state.data_inputs['ps_historico_1'] = st.number_input("P/S Histórico Año -2 (x)", min_value=0.0, value=st.session_state.data_inputs['ps_historico_1'], format="%.2f", help="P/S de hace dos años.")
        st.session_state.data_inputs['ps_historico_2'] = st.number_input("P/S Histórico Año -1 (x)", min_value=0.0, value=st.session_state.data_inputs['ps_historico_2'], format="%.2f", help="P/S del año pasado.")
        st.session_state.data_inputs['ps_historico_3'] = st.number_input("P/S Histórico Año Actual (x)", min_value=0.0, value=st.session_state.data_inputs['ps_historico_3'], format="%.2f", help="P/S del año actual.")

        st.session_state.data_inputs['pb_historico_1'] = st.number_input("P/B Histórico Año -2 (x)", min_value=0.0, value=st.session_state.data_inputs['pb_historico_1'], format="%.2f", help="P/B de hace dos años.")
        st.session_state.data_inputs['pb_historico_2'] = st.number_input("P/B Histórico Año -1 (x)", min_value=0.0, value=st.session_state.data_inputs['pb_historico_2'], format="%.2f", help="P/B del año pasado.")
        st.session_state.data_inputs['pb_historico_3'] = st.number_input("P/B Histórico Año Actual (x)", min_value=0.0, value=st.session_state.data_inputs['pb_historico_3'], format="%.2f", help="P/B del año actual.")

# Expander para organizar los escenarios de revenue estimado.
with st.expander("📉 Escenarios de Revenue Estimado", expanded=True):
    st.markdown("Define las estimaciones de ingresos para diferentes escenarios de mercado.")
    st.session_state.data_inputs['revenue_pesimista'] = st.number_input(
        "Revenue Estimado (Pesimista) ($)",
        min_value=0.0, value=st.session_state.data_inputs['revenue_pesimista'], format="%.2f",
        help="Estimación de ingresos para el escenario más conservador, considerando condiciones de mercado desfavorables."
    )
    st.session_state.data_inputs['revenue_base'] = st.number_input(
        "Revenue Estimado (Base) ($)",
        min_value=0.0, value=st.session_state.data_inputs['revenue_base'], format="%.2f",
        help="Estimación de ingresos para el escenario más probable, bajo condiciones de mercado normales."
    )
    st.session_state.data_inputs['revenue_optimista'] = st.number_input(
        "Revenue Estimado (Optimista) ($)",
        min_value=0.0, value=st.session_state.data_inputs['revenue_optimista'], format="%.2f",
        help="Estimación de ingresos para el escenario más favorable, asumiendo condiciones de mercado muy positivas."
    )

# Botón para ejecutar el análisis financiero.
st.markdown("---")
if st.button("🚀 Ejecutar Análisis Financiero", key="run_analysis_button", help="Haz clic para calcular todos los múltiplos, valuaciones y generar recomendaciones."):
    # Validar todos los inputs cruciales antes de proceder con los cálculos.
    inputs_validos = True
    # Lista de campos que deben ser estrictamente positivos para evitar divisiones por cero o cálculos sin sentido.
    campos_positivos_requeridos = [
        'precio_actual', 'eps_actual', 'eps_proyectado', 'revenue_actual',
        'net_income_estimado', 'acciones_circulacion', 'book_value_per_share',
        'equity_proyectado', 'wacc', 'per_esperado', 'ps_esperado', 'pb_esperado'
    ]
    # Campos que pueden ser cero pero no negativos
    campos_no_negativos_permitidos_cero = [
        'revenue_pesimista', 'revenue_base', 'revenue_optimista',
        'dividendos_anuales', 'tasa_crecimiento_esperada', 'margen_seguridad_deseado',
        'per_historico_1', 'per_historico_2', 'per_historico_3',
        'ps_historico_1', 'ps_historico_2', 'ps_historico_3',
        'pb_historico_1', 'pb_historico_2', 'pb_historico_3'
    ]

    # Realiza la validación para los campos estrictamente positivos
    for campo in campos_positivos_requeridos:
        if st.session_state.data_inputs[campo] <= 0:
            st.error(f"Error: El campo '{campo.replace('_', ' ').title()}' debe ser un valor positivo para realizar los cálculos. Por favor, corrígelo.")
            inputs_validos = False
    
    # Realiza la validación para los campos no negativos
    for campo in campos_no_negativos_permitidos_cero:
        if st.session_state.data_inputs[campo] < 0:
            st.error(f"Error: El campo '{campo.replace('_', ' ').title()}' no puede ser negativo. Por favor, corrígelo.")
            inputs_validos = False

    # Validación específica para WACC vs Tasa de Crecimiento Perpetuo
    if st.session_state.data_inputs['wacc'] <= st.session_state.data_inputs['tasa_crecimiento_perpetuo'] and st.session_state.data_inputs['wacc'] > 0:
        st.warning("Advertencia: Para el cálculo del Valor Terminal por Crecimiento Perpetuo, el WACC debe ser mayor que la Tasa de Crecimiento Perpetuo. Los resultados del DCF podrían ser inexactos o cero.")
        # No se detiene la ejecución, pero se advierte al usuario.

    if inputs_validos:
        st.success("¡Datos validados! Procediendo con el análisis financiero...")
        st.markdown("---")
        
        # Diccionario para almacenar todos los resultados para el reporte PDF y visualizaciones
        resultados_analisis = {
            'precio_actual': st.session_state.data_inputs['precio_actual'],
            'precio_obj_multiplos': 0.0,
            'precio_obj_dcf_pesimista': 0.0,
            'precio_obj_dcf_base': 0.0,
            'precio_obj_dcf_optimista': 0.0,
            'precio_obj_multiplo_terminal_pesimista': 0.0,
            'precio_obj_multiplo_terminal_base': 0.0,
            'precio_obj_multiplo_terminal_optimista': 0.0,
            'precio_justo_final': 0.0,
            'precio_maximo_a_pagar': 0.0,
            'recomendaciones_generales': [],
            'recomendaciones_multiplos': [],
            'fcf_proyectados_base': [],
            'pe_actual': 0.0,
            'ps_actual': 0.0,
            'pb_actual': 0.0,
            'pe_proyectado': 0.0,
            'ps_proyectado': 0.0,
            'pb_proyectado': 0.0,
        }

        # ===================== SECCIÓN: 2. CÁLCULO DE MÚLTIPLOS =====================
        st.header("2. Cálculo y Análisis de Múltiplos")
        st.markdown("---")

        # Cálculo de múltiplos actuales
        revenue_per_share_actual = st.session_state.data_inputs['revenue_actual'] / st.session_state.data_inputs['acciones_circulacion'] if st.session_state.data_inputs['acciones_circulacion'] > 0 else 0
        
        pe_actual = calcular_pe(st.session_state.data_inputs['precio_actual'], st.session_state.data_inputs['eps_actual'])
        ps_actual = calcular_ps(st.session_state.data_inputs['precio_actual'], revenue_per_share_actual)
        pb_actual = calcular_pb(st.session_state.data_inputs['precio_actual'], st.session_state.data_inputs['book_value_per_share'])

        # Cálculo de múltiplos proyectados
        # Para P/S proyectado, usamos el revenue base proyectado
        revenue_per_share_proyectado_base = st.session_state.data_inputs['revenue_base'] / st.session_state.data_inputs['acciones_circulacion'] if st.session_state.data_inputs['acciones_circulacion'] > 0 else 0
        
        pe_proyectado = calcular_pe(st.session_state.data_inputs['precio_actual'], st.session_state.data_inputs['eps_proyectado'])
        ps_proyectado = calcular_ps(st.session_state.data_inputs['precio_actual'], revenue_per_share_proyectado_base)
        pb_proyectado = calcular_pb(st.session_state.data_inputs['precio_actual'], st.session_state.data_inputs['equity_proyectado'] / st.session_state.data_inputs['acciones_circulacion'] if st.session_state.data_inputs['acciones_circulacion'] > 0 else 0)

        resultados_analisis['pe_actual'] = pe_actual
        resultados_analisis['ps_actual'] = ps_actual
        resultados_analisis['pb_actual'] = pb_actual
        resultados_analisis['pe_proyectado'] = pe_proyectado
        resultados_analisis['ps_proyectado'] = ps_proyectado
        resultados_analisis['pb_proyectado'] = pb_proyectado

        st.markdown("#### Múltiplos Calculados")
        multiplos_df = pd.DataFrame({
            "Múltiplo": ["P/E", "P/S", "P/B"],
            "Actual (x)": [f"{pe_actual:,.2f}", f"{ps_actual:,.2f}", f"{pb_actual:,.2f}"],
            "Proyectado (x)": [f"{pe_proyectado:,.2f}", f"{ps_proyectado:,.2f}", f"{pb_proyectado:,.2f}"]
        })
        st.table(multiplos_df)

        st.markdown("#### Interpretación de Múltiplos")
        # Interpretación de P/E
        if pe_proyectado > 0 and st.session_state.data_inputs['per_esperado'] > 0:
            if pe_proyectado < st.session_state.data_inputs['per_esperado'] * 0.9:
                resultados_analisis['recomendaciones_multiplos'].append(f"El PER proyectado ({pe_proyectado:,.2f}x) es significativamente menor que el PER esperado ({st.session_state.data_inputs['per_esperado']:,.2f}x), lo que sugiere que la acción podría estar **subvaluada** por PER.")
            elif pe_proyectado > st.session_state.data_inputs['per_esperado'] * 1.1:
                resultados_analisis['recomendaciones_multiplos'].append(f"El PER proyectado ({pe_proyectado:,.2f}x) es significativamente mayor que el PER esperado ({st.session_state.data_inputs['per_esperado']:,.2f}x), lo que sugiere que la acción podría estar **sobrevaluada** por PER.")
            else:
                resultados_analisis['recomendaciones_multiplos'].append(f"El PER proyectado ({pe_proyectado:,.2f}x) está en línea con el PER esperado ({st.session_state.data_inputs['per_esperado']:,.2f}x), indicando una valuación **neutral** por PER.")
        else:
            resultados_analisis['recomendaciones_multiplos'].append("No se puede interpretar el PER proyectado debido a datos insuficientes (EPS proyectado o PER esperado es cero).")

        # Interpretación de P/S
        if ps_proyectado > 0 and st.session_state.data_inputs['ps_esperado'] > 0:
            if ps_proyectado < st.session_state.data_inputs['ps_esperado'] * 0.9:
                resultados_analisis['recomendaciones_multiplos'].append(f"El P/S proyectado ({ps_proyectado:,.2f}x) es significativamente menor que el P/S esperado ({st.session_state.data_inputs['ps_esperado']:,.2f}x), lo que sugiere que la acción podría estar **subvaluada** por P/S.")
            elif ps_proyectado > st.session_state.data_inputs['ps_esperado'] * 1.1:
                resultados_analisis['recomendaciones_multiplos'].append(f"El P/S proyectado ({ps_proyectado:,.2f}x) es significativamente mayor que el P/S esperado ({st.session_state.data_inputs['ps_esperado']:,.2f}x), lo que sugiere que la acción podría estar **sobrevaluada** por P/S.")
            else:
                resultados_analisis['recomendaciones_multiplos'].append(f"El P/S proyectado ({ps_proyectado:,.2f}x) está en línea con el P/S esperado ({st.session_state.data_inputs['ps_esperado']:,.2f}x), indicando una valuación **neutral** por P/S.")
        else:
            resultados_analisis['recomendaciones_multiplos'].append("No se puede interpretar el P/S proyectado debido a datos insuficientes (Revenue por acción proyectado o P/S esperado es cero).")

        # Interpretación de P/B
        if pb_proyectado > 0 and st.session_state.data_inputs['pb_esperado'] > 0:
            if pb_proyectado < st.session_state.data_inputs['pb_esperado'] * 0.9:
                resultados_analisis['recomendaciones_multiplos'].append(f"El P/B proyectado ({pb_proyectado:,.2f}x) es significativamente menor que el P/B esperado ({st.session_state.data_inputs['pb_esperado']:,.2f}x), lo que sugiere que la acción podría estar **subvaluada** por P/B.")
            elif pb_proyectado > st.session_state.data_inputs['pb_esperado'] * 1.1:
                resultados_analisis['recomendaciones_multiplos'].append(f"El P/B proyectado ({pb_proyectado:,.2f}x) es significativamente mayor que el P/B esperado ({st.session_state.data_inputs['pb_esperado']:,.2f}x), lo que sugiere que la acción podría estar **sobrevaluada** por P/B.")
            else:
                resultados_analisis['recomendaciones_multiplos'].append(f"El P/B proyectado ({pb_proyectado:,.2f}x) está en línea con el P/B esperado ({st.session_state.data_inputs['pb_esperado']:,.2f}x), indicando una valuación **neutral** por P/B.")
        else:
            resultados_analisis['recomendaciones_multiplos'].append("No se puede interpretar el P/B proyectado debido a datos insuficientes (Book Value por acción proyectado o P/B esperado es cero).")

        for rec in resultados_analisis['recomendaciones_multiplos']:
            st.info(rec)

        # Gráfico de Múltiplos Históricos vs Proyectados
        st.markdown("---")
        st.subheader("Gráfico de Múltiplos Históricos vs Proyectados")
        
        m_names = ['PER', 'P/S', 'P/B']
        m_actual = [pe_actual, ps_actual, pb_actual]
        m_proyectado = [pe_proyectado, ps_proyectado, pb_proyectado]
        m_esperado = [st.session_state.data_inputs['per_esperado'], st.session_state.data_inputs['ps_esperado'], st.session_state.data_inputs['pb_esperado']]
        m_hist_1 = [st.session_state.data_inputs['per_historico_1'], st.session_state.data_inputs['ps_historico_1'], st.session_state.data_inputs['pb_historico_1']]
        m_hist_2 = [st.session_state.data_inputs['per_historico_2'], st.session_state.data_inputs['ps_historico_2'], st.session_state.data_inputs['pb_historico_2']]
        m_hist_3 = [st.session_state.data_inputs['per_historico_3'], st.session_state.data_inputs['ps_historico_3'], st.session_state.data_inputs['pb_historico_3']]

        fig_multiplos = go.Figure()

        fig_multiplos.add_trace(go.Bar(
            name='Actual',
            x=m_names, y=m_actual,
            marker_color='#e94560' # Color de acento
        ))
        fig_multiplos.add_trace(go.Bar(
            name='Proyectado',
            x=m_names, y=m_proyectado,
            marker_color='#533483' # Color secundario
        ))
        fig_multiplos.add_trace(go.Scatter(
            name='Esperado',
            x=m_names, y=m_esperado,
            mode='markers+lines',
            marker=dict(size=10, color='#0f3460'), # Color oscuro
            line=dict(width=2, dash='dot', color='#0f3460')
        ))
        fig_multiplos.add_trace(go.Scatter(
            name='Histórico Año -2',
            x=m_names, y=m_hist_1,
            mode='markers+lines',
            marker=dict(size=8, color='#8c8c8c'),
            line=dict(width=1, dash='dash', color='#8c8c8c')
        ))
        fig_multiplos.add_trace(go.Scatter(
            name='Histórico Año -1',
            x=m_names, y=m_hist_2,
            mode='markers+lines',
            marker=dict(size=8, color='#b0b0b0'),
            line=dict(width=1, dash='dash', color='#b0b0b0')
        ))
        fig_multiplos.add_trace(go.Scatter(
            name='Histórico Año Actual',
            x=m_names, y=m_hist_3,
            mode='markers+lines',
            marker=dict(size=8, color='#d0d0d0'),
            line=dict(width=1, dash='dash', color='#d0d0d0')
        ))

        fig_multiplos.update_layout(
            title_text='Comparación de Múltiplos (Actual, Proyectado, Esperado e Histórico)',
            xaxis_title='Múltiplo',
            yaxis_title='Valor (x)',
            barmode='group',
            plot_bgcolor='#1a1a2e', # Fondo del gráfico
            paper_bgcolor='#1a1a2e', # Fondo del papel
            font_color='#e0e0e0', # Color del texto
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_multiplos, use_container_width=True)

        # Detección de múltiplos fuera del promedio histórico
        st.markdown("---")
        st.subheader("Análisis de Tendencia de Múltiplos")
        multiplos_historicos_per = [st.session_state.data_inputs['per_historico_1'], st.session_state.data_inputs['per_historico_2'], st.session_state.data_inputs['per_historico_3']]
        multiplos_historicos_ps = [st.session_state.data_inputs['ps_historico_1'], st.session_state.data_inputs['ps_historico_2'], st.session_state.data_inputs['ps_historico_3']]
        multiplos_historicos_pb = [st.session_state.data_inputs['pb_historico_1'], st.session_state.data_inputs['pb_historico_2'], st.session_state.data_inputs['pb_historico_3']]

        if all(m > 0 for m in multiplos_historicos_per):
            avg_per_hist = np.mean(multiplos_historicos_per)
            if pe_proyectado > avg_per_hist * 1.2:
                st.warning(f"El PER proyectado ({pe_proyectado:,.2f}x) está significativamente por encima del promedio histórico ({avg_per_hist:,.2f}x). Esto podría indicar una sobrevaluación o altas expectativas de crecimiento.")
            elif pe_proyectado < avg_per_hist * 0.8:
                st.info(f"El PER proyectado ({pe_proyectado:,.2f}x) está significativamente por debajo del promedio histórico ({avg_per_hist:,.2f}x). Esto podría indicar una subvaluación o que el mercado tiene bajas expectativas.")
            else:
                st.success(f"El PER proyectado ({pe_proyectado:,.2f}x) está en línea con el promedio histórico ({avg_per_hist:,.2f}x), lo que sugiere una valuación consistente.")
        else:
            st.info("No hay suficientes datos históricos de PER para un análisis de tendencia.")

        if all(m > 0 for m in multiplos_historicos_ps):
            avg_ps_hist = np.mean(multiplos_historicos_ps)
            if ps_proyectado > avg_ps_hist * 1.2:
                st.warning(f"El P/S proyectado ({ps_proyectado:,.2f}x) está significativamente por encima del promedio histórico ({avg_ps_hist:,.2f}x).")
            elif ps_proyectado < avg_ps_hist * 0.8:
                st.info(f"El P/S proyectado ({ps_proyectado:,.2f}x) está significativamente por debajo del promedio histórico ({avg_ps_hist:,.2f}x).")
            else:
                st.success(f"El P/S proyectado ({ps_proyectado:,.2f}x) está en línea con el promedio histórico ({avg_ps_hist:,.2f}x).")
        else:
            st.info("No hay suficientes datos históricos de P/S para un análisis de tendencia.")

        if all(m > 0 for m in multiplos_historicos_pb):
            avg_pb_hist = np.mean(multiplos_historicos_pb)
            if pb_proyectado > avg_pb_hist * 1.2:
                st.warning(f"El P/B proyectado ({pb_proyectado:,.2f}x) está significativamente por encima del promedio histórico ({avg_pb_hist:,.2f}x).")
            elif pb_proyectado < avg_pb_hist * 0.8:
                st.info(f"El P/B proyectado ({pb_proyectado:,.2f}x) está significativamente por debajo del promedio histórico ({avg_pb_hist:,.2f}x).")
            else:
                st.success(f"El P/B proyectado ({pb_proyectado:,.2f}x) está en línea con el promedio histórico ({avg_pb_hist:,.2f}x).")
        else:
            st.info("No hay suficientes datos históricos de P/B para un análisis de tendencia.")

        # ===================== SECCIÓN: 3. VALUACIÓN POR ESCENARIOS =====================
        st.header("3. Valuación por Escenarios")
        st.markdown("---")
        
        # Pestañas para organizar los métodos de valuación
        tab_dcf, tab_multiplos_terminal, tab_resumen_escenarios = st.tabs(["DCF (Crecimiento Perpetuo)", "Múltiplo Terminal", "Resumen Escenarios"])

        with tab_dcf:
            st.markdown("### Descuento de Flujos de Caja (DCF) - Método de Crecimiento Perpetuo")
            st.markdown("Este método proyecta los flujos de caja libres de la empresa y los descuenta al presente, asumiendo un crecimiento perpetuo después de un período explícito.")
            
            # Escenario Pesimista (DCF)
            st.markdown("#### Escenario Pesimista")
            precio_obj_dcf_pesimista, fcf_pesimista = valuacion_dcf(st.session_state.data_inputs, "Pesimista", factor_crecimiento=0.7, factor_wacc=1.2)
            resultados_analisis['precio_obj_dcf_pesimista'] = precio_obj_dcf_pesimista
            
            # Escenario Base (DCF)
            st.markdown("#### Escenario Base")
            precio_obj_dcf_base, fcf_base = valuacion_dcf(st.session_state.data_inputs, "Base", factor_crecimiento=1.0, factor_wacc=1.0)
            resultados_analisis['precio_obj_dcf_base'] = precio_obj_dcf_base
            resultados_analisis['fcf_proyectados_base'] = fcf_base # Guardar para el PDF

            # Escenario Optimista (DCF)
            st.markdown("#### Escenario Optimista")
            precio_obj_dcf_optimista, fcf_optimista = valuacion_dcf(st.session_state.data_inputs, "Optimista", factor_crecimiento=1.3, factor_wacc=0.8)
            resultados_analisis['precio_obj_dcf_optimista'] = precio_obj_dcf_optimista

        with tab_multiplos_terminal:
            st.markdown("### Valuación por Múltiplo Terminal")
            st.markdown("Este método estima el valor de la empresa al final del período de proyección explícita, aplicando un múltiplo de valoración (ej. PER) a una métrica financiera proyectada.")

            # Escenario Pesimista (Múltiplo Terminal)
            st.markdown("#### Escenario Pesimista")
            precio_obj_multiplo_terminal_pesimista = valuacion_multiplo_terminal(st.session_state.data_inputs, "Pesimista", factor_crecimiento=0.7, factor_wacc=1.2)
            resultados_analisis['precio_obj_multiplo_terminal_pesimista'] = precio_obj_multiplo_terminal_pesimista

            # Escenario Base (Múltiplo Terminal)
            st.markdown("#### Escenario Base")
            precio_obj_multiplo_terminal_base = valuacion_multiplo_terminal(st.session_state.data_inputs, "Base", factor_crecimiento=1.0, factor_wacc=1.0)
            resultados_analisis['precio_obj_multiplo_terminal_base'] = precio_obj_multiplo_terminal_base

            # Escenario Optimista (Múltiplo Terminal)
            st.markdown("#### Escenario Optimista")
            precio_obj_multiplo_terminal_optimista = valuacion_multiplo_terminal(st.session_state.data_inputs, "Optimista", factor_crecimiento=1.3, factor_wacc=0.8)
            resultados_analisis['precio_obj_multiplo_terminal_optimista'] = precio_obj_multiplo_terminal_optimista

        with tab_resumen_escenarios:
            st.markdown("### Resumen de Precios Objetivos por Escenario")
            st.markdown("Aquí puedes ver una consolidación de los precios objetivos calculados para cada escenario y método de valuación.")

            precios_dcf = {
                "Pesimista": resultados_analisis['precio_obj_dcf_pesimista'],
                "Base": resultados_analisis['precio_obj_dcf_base'],
                "Optimista": resultados_analisis['precio_obj_dcf_optimista']
            }
            precios_multiplo_terminal = {
                "Pesimista": resultados_analisis['precio_obj_multiplo_terminal_pesimista'],
                "Base": resultados_analisis['precio_obj_multiplo_terminal_base'],
                "Optimista": resultados_analisis['precio_obj_multiplo_terminal_optimista']
            }

            # DataFrame para la tabla de resumen
            resumen_df = pd.DataFrame({
                "Escenario": ["Pesimista", "Base", "Optimista"],
                "Precio Objetivo DCF ($)": [f"{v:,.2f}" for v in precios_dcf.values()],
                "Precio Objetivo Múltiplo Terminal ($)": [f"{v:,.2f}" for v in precios_multiplo_terminal.values()]
            })
            st.table(resumen_df)

            # Gráfico de precios justos por escenario
            st.markdown("---")
            st.subheader("Gráfico de Precios Justos por Escenario")
            
            escenarios = list(precios_dcf.keys())
            valores_dcf = list(precios_dcf.values())
            valores_multiplo_terminal = list(precios_multiplo_terminal.values())

            fig_escenarios = go.Figure()
            fig_escenarios.add_trace(go.Bar(
                name='DCF (Crecimiento Perpetuo)',
                x=escenarios, y=valores_dcf,
                marker_color='#e94560'
            ))
            fig_escenarios.add_trace(go.Bar(
                name='Múltiplo Terminal',
                x=escenarios, y=valores_multiplo_terminal,
                marker_color='#533483'
            ))
            fig_escenarios.add_trace(go.Scatter(
                name='Precio Actual',
                x=escenarios, y=[st.session_state.data_inputs['precio_actual']] * len(escenarios),
                mode='lines',
                line=dict(color='#0f3460', dash='dash', width=3),
                marker=dict(size=10)
            ))

            fig_escenarios.update_layout(
                title_text='Precios Objetivos por Escenario de Valuación',
                xaxis_title='Escenario',
                yaxis_title='Precio por Acción ($)',
                barmode='group',
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#1a1a2e',
                font_color='#e0e0e0',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_escenarios, use_container_width=True)

        # ===================== SECCIÓN: 4. RECOMENDACIONES FINALES =====================
        st.header("4. Resumen de Valuación y Recomendaciones")
        st.markdown("---")

        # Calcular precio objetivo promedio ponderado (ej. 50% DCF Base, 50% Múltiplos Promedio)
        # Se puede ajustar la ponderación según la preferencia del usuario o la robustez de los datos
        precio_obj_multiplos_promedio = valuacion_por_multiplos(st.session_state.data_inputs)
        resultados_analisis['precio_obj_multiplos'] = precio_obj_multiplos_promedio

        # Consideramos un promedio simple entre los métodos principales para el precio justo final
        precios_para_promedio = []
        if resultados_analisis['precio_obj_dcf_base'] > 0:
            precios_para_promedio.append(resultados_analisis['precio_obj_dcf_base'])
        if resultados_analisis['precio_obj_multiplo_terminal_base'] > 0:
            precios_para_promedio.append(resultados_analisis['precio_obj_multiplo_terminal_base'])
        if precio_obj_multiplos_promedio > 0:
            precios_para_promedio.append(precio_obj_multiplos_promedio)
        
        if precios_para_promedio:
            precio_justo_final = np.mean(precios_para_promedio)
            st.success(f"**Precio Justo Final Estimado (Promedio Ponderado de Métodos):** ${precio_justo_final:,.2f}")
        else:
            precio_justo_final = 0.0
            st.warning("No se pudo calcular un precio justo final. Asegúrate de que los métodos de valuación generen resultados válidos.")
        
        resultados_analisis['precio_justo_final'] = precio_justo_final

        # Calcular precio máximo a pagar con margen de seguridad
        margen_seguridad_decimal = st.session_state.data_inputs['margen_seguridad_deseado'] / 100
        precio_maximo_a_pagar = precio_justo_final * (1 - margen_seguridad_decimal)
        
        if precio_justo_final > 0:
            st.success(f"**Precio Máximo a Pagar (con Margen de Seguridad del {st.session_state.data_inputs['margen_seguridad_deseado']:.2f}%):** ${precio_maximo_a_pagar:,.2f}")
        else:
            st.info("No se puede calcular el precio máximo a pagar sin un precio justo final válido.")

        resultados_analisis['precio_maximo_a_pagar'] = precio_maximo_a_pagar

        st.markdown("#### Recomendaciones Generales")
        # Generar mensajes de recomendación basados en los resultados
        if precio_justo_final > 0:
            if st.session_state.data_inputs['precio_actual'] < precio_maximo_a_pagar and precio_maximo_a_pagar > 0:
                margen_actual = ((precio_justo_final - st.session_state.data_inputs['precio_actual']) / precio_justo_final) * 100
                resultados_analisis['recomendaciones_generales'].append(f"Esta acción parece **subvaluada** en el escenario base con un margen del {margen_actual:,.2f}% respecto al precio justo. El precio actual (${st.session_state.data_inputs['precio_actual']:,.2f}) está por debajo del precio máximo a pagar (${precio_maximo_a_pagar:,.2f}).")
                st.markdown(f"✅ **¡Oportunidad Potencial!** Esta acción parece **subvaluada** en el escenario base con un margen del **{margen_actual:,.2f}%** respecto al precio justo. El precio actual (${st.session_state.data_inputs['precio_actual']:,.2f}) está por debajo del precio máximo a pagar (${precio_maximo_a_pagar:,.2f}).")
            elif st.session_state.data_inputs['precio_actual'] > precio_justo_final * 1.1: # Más del 10% sobre el precio justo
                resultados_analisis['recomendaciones_generales'].append(f"Esta acción parece **sobrevaluada**. El precio actual (${st.session_state.data_inputs['precio_actual']:,.2f}) es significativamente más alto que el precio justo estimado (${precio_justo_final:,.2f}).")
                st.markdown(f"❌ **¡Precaución!** Esta acción parece **sobrevaluada**. El precio actual (${st.session_state.data_inputs['precio_actual']:,.2f}) es significativamente más alto que el precio justo estimado (${precio_justo_final:,.2f}).")
            else:
                resultados_analisis['recomendaciones_generales'].append(f"La acción parece tener una valuación **neutral**. El precio actual (${st.session_state.data_inputs['precio_actual']:,.2f}) está cerca del precio justo estimado (${precio_justo_final:,.2f}).")
                st.markdown(f" neutral. El precio actual (${st.session_state.data_inputs['precio_actual']:,.2f}) está cerca del precio justo estimado (${precio_justo_final:,.2f}).")
        else:
            resultados_analisis['recomendaciones_generales'].append("No se puede generar una recomendación de valuación final debido a la falta de un precio justo estimado.")
            st.info("No se puede generar una recomendación de valuación final debido a la falta de un precio justo estimado.")

        # Recomendaciones basadas en escenarios
        if resultados_analisis['precio_obj_dcf_pesimista'] > 0:
            resultados_analisis['recomendaciones_generales'].append(f"Considera tu tolerancia al riesgo: Evita invertir si no estás cómodo con un escenario pesimista con un precio estimado de ${resultados_analisis['precio_obj_dcf_pesimista']:,.2f} (DCF).")
            st.warning(f"Considera tu tolerancia al riesgo: Evita invertir si no estás cómodo con un escenario pesimista con un precio estimado de **${resultados_analisis['precio_obj_dcf_pesimista']:,.2f}** (DCF).")
        
        if resultados_analisis['precio_obj_dcf_optimista'] > 0:
            resultados_analisis['recomendaciones_generales'].append(f"El escenario optimista proyecta un precio de ${resultados_analisis['precio_obj_dcf_optimista']:,.2f} (DCF), lo que indica un potencial alcista significativo si las condiciones son favorables.")
            st.info(f"El escenario optimista proyecta un precio de **${resultados_analisis['precio_obj_dcf_optimista']:,.2f}** (DCF), lo que indica un potencial alcista significativo si las condiciones son favorables.")

        # ===================== SECCIÓN: 5. VISUALIZACIONES ADICIONALES =====================
        st.header("5. Visualizaciones Adicionales")
        st.markdown("---")

        # Gráfico de comparación entre precio actual y precio estimado
        st.subheader("Comparación: Precio Actual vs. Precios Estimados")
        fig_comparacion = go.Figure()

        fig_comparacion.add_trace(go.Bar(
            name='Precio Actual',
            x=['Precio Actual'], y=[st.session_state.data_inputs['precio_actual']],
            marker_color='#e94560'
        ))
        fig_comparacion.add_trace(go.Bar(
            name='Precio Justo Final',
            x=['Precio Justo Final'], y=[precio_justo_final],
            marker_color='#533483'
        ))
        if precio_maximo_a_pagar > 0:
            fig_comparacion.add_trace(go.Bar(
                name=f'Precio Máximo a Pagar (Margen {st.session_state.data_inputs["margen_seguridad_deseado"]:.0f}%)',
                x=['Precio Máximo a Pagar'], y=[precio_maximo_a_pagar],
                marker_color='#0f3460'
            ))

        fig_comparacion.update_layout(
            title_text='Comparación de Precios: Actual vs. Estimados',
            yaxis_title='Precio por Acción ($)',
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#1a1a2e',
            font_color='#e0e0e0',
            showlegend=True
        )
        st.plotly_chart(fig_comparacion, use_container_width=True)

        # Tabla de resumen de resultados y métricas clave
        st.markdown("---")
        st.subheader("Resumen de Resultados y Métricas Clave")
        
        resumen_data = {
            "Métrica": [
                "Precio Actual",
                "EPS Actual",
                "EPS Proyectado",
                "Revenue Actual",
                "Net Income Estimado",
                "Acciones en Circulación",
                "Dividendos Anuales",
                "Book Value per Share",
                "Equity Proyectado",
                "Tasa de Crecimiento Esperada",
                "WACC / Tasa de Descuento",
                "Margen de Seguridad Deseado",
                "Años de Proyección DCF",
                "Tasa Crecimiento Perpetuo",
                "PER Esperado",
                "P/S Esperado",
                "P/B Esperado",
                "PER Actual",
                "P/S Actual",
                "P/B Actual",
                "PER Proyectado",
                "P/S Proyectado",
                "P/B Proyectado",
                "Precio Objetivo P/E",
                "Precio Objetivo P/S",
                "Precio Objetivo P/B",
                "Precio Objetivo Promedio por Múltiplos",
                "Precio Objetivo DCF (Pesimista)",
                "Precio Objetivo DCF (Base)",
                "Precio Objetivo DCF (Optimista)",
                "Precio Objetivo Múltiplo Terminal (Pesimista)",
                "Precio Objetivo Múltiplo Terminal (Base)",
                "Precio Objetivo Múltiplo Terminal (Optimista)",
                "Precio Justo Final (Promedio Ponderado)",
                "Precio Máximo a Pagar (con Margen de Seguridad)"
            ],
            "Valor": [
                f"${st.session_state.data_inputs['precio_actual']:,.2f}",
                f"${st.session_state.data_inputs['eps_actual']:,.2f}",
                f"${st.session_state.data_inputs['eps_proyectado']:,.2f}",
                f"${st.session_state.data_inputs['revenue_actual']:,.2f}",
                f"${st.session_state.data_inputs['net_income_estimado']:,.2f}",
                f"{st.session_state.data_inputs['acciones_circulacion']:,.0f}",
                f"${st.session_state.data_inputs['dividendos_anuales']:,.2f}",
                f"${st.session_state.data_inputs['book_value_per_share']:,.2f}",
                f"${st.session_state.data_inputs['equity_proyectado']:,.2f}",
                f"{st.session_state.data_inputs['tasa_crecimiento_esperada']:.2f}%",
                f"{st.session_state.data_inputs['wacc']:.2f}%",
                f"{st.session_state.data_inputs['margen_seguridad_deseado']:.2f}%",
                f"{st.session_state.data_inputs['años_proyeccion_dcf']}",
                f"{st.session_state.data_inputs['tasa_crecimiento_perpetuo']:.2f}%",
                f"{st.session_state.data_inputs['per_esperado']:.2f}x",
                f"{st.session_state.data_inputs['ps_esperado']:.2f}x",
                f"{st.session_state.data_inputs['pb_esperado']:.2f}x",
                f"{pe_actual:.2f}x",
                f"{ps_actual:.2f}x",
                f"{pb_actual:.2f}x",
                f"{pe_proyectado:.2f}x",
                f"{ps_proyectado:.2f}x",
                f"{pb_proyectado:.2f}x",
                f"${st.session_state.data_inputs['eps_proyectado'] * st.session_state.data_inputs['per_esperado'] if st.session_state.data_inputs['eps_proyectado'] > 0 and st.session_state.data_inputs['per_esperado'] > 0 else 0.0:,.2f}",
                f"${(st.session_state.data_inputs['revenue_base'] / st.session_state.data_inputs['acciones_circulacion']) * st.session_state.data_inputs['ps_esperado'] if st.session_state.data_inputs['acciones_circulacion'] > 0 and st.session_state.data_inputs['revenue_base'] > 0 and st.session_state.data_inputs['ps_esperado'] > 0 else 0.0:,.2f}",
                f"${(st.session_state.data_inputs['equity_proyectado'] / st.session_state.data_inputs['acciones_circulacion']) * st.session_state.data_inputs['pb_esperado'] if st.session_state.data_inputs['equity_proyectado'] > 0 and st.session_state.data_inputs['acciones_circulacion'] > 0 and st.session_state.data_inputs['pb_esperado'] > 0 else 0.0:,.2f}",
                f"${resultados_analisis['precio_obj_multiplos']:,.2f}",
                f"${resultados_analisis['precio_obj_dcf_pesimista']:,.2f}",
                f"${resultados_analisis['precio_obj_dcf_base']:,.2f}",
                f"${resultados_analisis['precio_obj_dcf_optimista']:,.2f}",
                f"${resultados_analisis['precio_obj_multiplo_terminal_pesimista']:,.2f}",
                f"${resultados_analisis['precio_obj_multiplo_terminal_base']:,.2f}",
                f"${resultados_analisis['precio_obj_multiplo_terminal_optimista']:,.2f}",
                f"${resultados_analisis['precio_justo_final']:,.2f}",
                f"${resultados_analisis['precio_maximo_a_pagar']:,.2f}"
            ]
        }
        resumen_df_final = pd.DataFrame(resumen_data)
        st.table(resumen_df_final)

        # ===================== SECCIÓN: 6. GENERACIÓN DE REPORTE PDF =====================
        st.header("6. Generación de Reporte PDF")
        st.markdown("---")
        st.info("Haz clic en el botón para generar un reporte PDF detallado con todos los datos y resultados del análisis.")
        if st.button("📄 Generar Reporte PDF", key="generate_pdf_button", help="Crea un archivo PDF con un resumen completo de este análisis."):
            generar_reporte_pdf(st.session_state.data_inputs, resultados_analisis)

    else:
        st.error("Por favor, corrige los errores en los datos de entrada para ejecutar el análisis.")

