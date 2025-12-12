"""
Dashboard 3D Interactivo ULTRA - SCE Gemelo Digital
Control Total: Nivel, Temperatura, Presión, Caudales, y más
"""
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import os
import sys

# Agregar path para importar módulos del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simuladores.simulador_tanque import TanqueSimulado, SensorUltrasonico, SensorAmbiental

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="SCE 3D ULTRA - Control Total",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2ca02c;
        border-color: #2ca02c;
    }
    .control-section {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES ====================

@st.cache_data(ttl=2)
def cargar_datos_historicos():
    """Cargar datos históricos desde SQLite"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(base_dir, "datos", "datos_sce.db")

    if not os.path.exists(db_path):
        return pd.DataFrame()

    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM mediciones ORDER BY id DESC LIMIT 1000"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

    return df

@st.cache_data(ttl=60)
def _calcular_geometria_tanque(altura_max, diametro):
    """
    Calcula arrays numpy estáticos para la geometría del tanque.
    Se cachean para evitar recalcular en cada renderizado.
    """
    radio = diametro / 2
    theta = np.linspace(0, 2*np.pi, 50)
    z_cilindro = np.linspace(0, altura_max, 50)
    theta_grid, z_grid = np.meshgrid(theta, z_cilindro)
    x_cilindro = radio * np.cos(theta_grid)
    y_cilindro = radio * np.sin(theta_grid)

    return {
        'radio': radio,
        'theta': theta,
        'z_grid': z_grid,
        'x_cilindro': x_cilindro,
        'y_cilindro': y_cilindro
    }

def crear_tanque_3d(nivel_actual, altura_max=200, diametro=100, umbral_bajo=30, umbral_alto=170,
                    caudal_entrada=0, caudal_salida=0, valvula_entrada=False, bomba_salida=False):
    """
    Crea visualización 3D del tanque con agua, tuberías y flujo
    """
    # Obtener geometría cacheada
    geom = _calcular_geometria_tanque(altura_max, diametro)
    radio = geom['radio']
    theta = geom['theta']
    z_grid = geom['z_grid']
    x_cilindro = geom['x_cilindro']
    y_cilindro = geom['y_cilindro']

    # Crear agua (cilindro de agua hasta el nivel actual)
    z_agua = np.linspace(0, max(nivel_actual, 1), 30)
    theta_agua, z_agua_grid = np.meshgrid(theta, z_agua)
    x_agua = radio * 0.95 * np.cos(theta_agua)
    y_agua = radio * 0.95 * np.sin(theta_agua)

    # Superficie del agua
    x_superficie = radio * 0.95 * np.cos(theta)
    y_superficie = radio * 0.95 * np.sin(theta)
    z_superficie = np.full_like(x_superficie, nivel_actual)

    # Crear figura
    fig = go.Figure()

    # Paredes del tanque (transparente)
    fig.add_trace(go.Surface(
        x=x_cilindro, y=y_cilindro, z=z_grid,
        colorscale=[[0, 'rgba(100, 100, 100, 0.2)'], [1, 'rgba(100, 100, 100, 0.2)']],
        showscale=False,
        name='Tanque',
        hoverinfo='skip'
    ))

    # Agua (cilindro azul)
    fig.add_trace(go.Surface(
        x=x_agua, y=y_agua, z=z_agua_grid,
        colorscale=[[0, 'rgba(30, 144, 255, 0.7)'], [1, 'rgba(0, 100, 255, 0.7)']],
        showscale=False,
        name='Agua',
        hoverinfo='skip'
    ))

    # Superficie del agua
    fig.add_trace(go.Scatter3d(
        x=x_superficie, y=y_superficie, z=z_superficie,
        mode='lines',
        line=dict(color='blue', width=3),
        name=f'Nivel: {nivel_actual:.1f} cm',
        showlegend=True
    ))

    # ==========TUBERÍA DE ENTRADA (ARRIBA) ==========
    # Posición: en la parte superior del tanque
    tuberia_entrada_x = [radio * 1.2, radio * 1.2]
    tuberia_entrada_y = [0, 0]
    tuberia_entrada_z = [altura_max * 0.9, altura_max * 1.15]

    # Color según estado
    color_entrada = 'green' if valvula_entrada else 'gray'
    width_entrada = 8 if valvula_entrada else 4

    fig.add_trace(go.Scatter3d(
        x=tuberia_entrada_x,
        y=tuberia_entrada_y,
        z=tuberia_entrada_z,
        mode='lines+markers',
        line=dict(color=color_entrada, width=width_entrada),
        marker=dict(size=6, color=color_entrada),
        name=f'Entrada: {caudal_entrada:.1f} L/min',
        showlegend=True
    ))

    # Indicador simple de flujo de entrada (optimizado - máximo 2 gotas)
    if valvula_entrada and caudal_entrada > 0:
        # Solo 1-2 gotas para mejor rendimiento
        n_gotas = min(int(caudal_entrada / 30), 2)
        if n_gotas > 0:
            for i in range(n_gotas):
                offset = i * (altura_max * 0.15)
                gota_z = altura_max * 0.9 - offset
                if gota_z > nivel_actual:
                    fig.add_trace(go.Scatter3d(
                        x=[radio * 1.2],
                        y=[0],
                        z=[gota_z],
                        mode='markers',
                        marker=dict(size=6, color='cyan', symbol='diamond'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

    # Conexión horizontal de entrada
    fig.add_trace(go.Scatter3d(
        x=[radio * 1.2, radio],
        y=[0, 0],
        z=[altura_max * 0.9, altura_max * 0.9],
        mode='lines',
        line=dict(color=color_entrada, width=width_entrada),
        showlegend=False,
        hoverinfo='skip'
    ))

    # ==========TUBERÍA DE SALIDA (ABAJO) ==========
    # Posición: en la parte inferior del tanque
    tuberia_salida_x = [radio * 1.2, radio * 1.2]
    tuberia_salida_y = [0, 0]
    tuberia_salida_z = [altura_max * 0.1, -altura_max * 0.15]

    # Color según estado
    color_salida = 'red' if bomba_salida else 'gray'
    width_salida = 8 if bomba_salida else 4

    fig.add_trace(go.Scatter3d(
        x=tuberia_salida_x,
        y=tuberia_salida_y,
        z=tuberia_salida_z,
        mode='lines+markers',
        line=dict(color=color_salida, width=width_salida),
        marker=dict(size=6, color=color_salida),
        name=f'Salida: {caudal_salida:.1f} L/min',
        showlegend=True
    ))

    # Indicador simple de flujo de salida (optimizado - máximo 2 gotas)
    if bomba_salida and caudal_salida > 0 and nivel_actual > altura_max * 0.1:
        # Solo 1-2 gotas para mejor rendimiento
        n_gotas = min(int(caudal_salida / 30), 2)
        if n_gotas > 0:
            for i in range(n_gotas):
                offset = i * (altura_max * 0.15)
                gota_z = altura_max * 0.1 - offset
                if gota_z > -altura_max * 0.15:
                    fig.add_trace(go.Scatter3d(
                        x=[radio * 1.2],
                        y=[0],
                        z=[gota_z],
                        mode='markers',
                        marker=dict(size=6, color='lightcoral', symbol='diamond'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

    # Conexión horizontal de salida
    fig.add_trace(go.Scatter3d(
        x=[radio, radio * 1.2],
        y=[0, 0],
        z=[altura_max * 0.1, altura_max * 0.1],
        mode='lines',
        line=dict(color=color_salida, width=width_salida),
        showlegend=False,
        hoverinfo='skip'
    ))

    # ========== UMBRALES ==========
    x_umbral_alto = radio * 1.1 * np.cos(theta)
    y_umbral_alto = radio * 1.1 * np.sin(theta)
    z_umbral_alto = np.full_like(x_umbral_alto, umbral_alto)

    fig.add_trace(go.Scatter3d(
        x=x_umbral_alto, y=y_umbral_alto, z=z_umbral_alto,
        mode='lines',
        line=dict(color='red', width=4, dash='dash'),
        name=f'Umbral Alto: {umbral_alto} cm'
    ))

    x_umbral_bajo = radio * 1.1 * np.cos(theta)
    y_umbral_bajo = radio * 1.1 * np.sin(theta)
    z_umbral_bajo = np.full_like(x_umbral_bajo, umbral_bajo)

    fig.add_trace(go.Scatter3d(
        x=x_umbral_bajo, y=y_umbral_bajo, z=z_umbral_bajo,
        mode='lines',
        line=dict(color='orange', width=4, dash='dash'),
        name=f'Umbral Bajo: {umbral_bajo} cm'
    ))

    # Configuración de layout
    flujo_neto = caudal_entrada - caudal_salida if valvula_entrada or bomba_salida else 0
    flujo_text = f" | Flujo: {flujo_neto:+.1f} L/min" if abs(flujo_neto) > 0.1 else ""

    fig.update_layout(
        title=dict(
            text=f"🌊 Tanque 3D - Nivel: {nivel_actual:.2f} cm ({(nivel_actual/altura_max)*100:.1f}%){flujo_text}",
            font=dict(size=18)
        ),
        scene=dict(
            xaxis=dict(title='X (cm)', range=[-radio*1.5, radio*1.5]),
            yaxis=dict(title='Y (cm)', range=[-radio*1.5, radio*1.5]),
            zaxis=dict(title='Altura (cm)', range=[-altura_max*0.2, altura_max*1.2]),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2),
                center=dict(x=0, y=0, z=0.3)
            ),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=2)
        ),
        height=700,
        showlegend=True,
        legend=dict(x=0.7, y=0.95),
        margin=dict(l=0, r=0, t=40, b=0),
        # Optimizaciones para rendimiento y anti-flickering
        uirevision='constant',  # Mantener estado de la UI entre actualizaciones
        transition=dict(duration=0),  # Sin animaciones de transición
        hovermode=False,  # Deshabilitar hover para mejor rendimiento
        dragmode='orbit'  # Modo de arrastre optimizado para 3D
    )

    return fig

def crear_gauge_nivel(nivel, altura_max=200):
    """Medidor tipo gauge para el nivel"""
    porcentaje = (nivel / altura_max) * 100

    if nivel < 30:
        color = "orange"
    elif nivel > 170:
        color = "red"
    else:
        color = "green"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=nivel,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Nivel (cm)", 'font': {'size': 24}},
        delta={'reference': altura_max/2, 'increasing': {'color': "blue"}},
        gauge={
            'axis': {'range': [None, altura_max], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(255, 165, 0, 0.3)'},
                {'range': [30, 170], 'color': 'rgba(0, 255, 0, 0.2)'},
                {'range': [170, altura_max], 'color': 'rgba(255, 0, 0, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 170
            }
        }
    ))

    fig.update_layout(height=400, margin=dict(l=20, r=20, t=60, b=20))
    return fig

def crear_grafica_historia(historia, titulo, color, unidad):
    """Crea gráfica de historia temporal"""
    fig = go.Figure()

    if len(historia) > 0:
        fig.add_trace(go.Scatter(
            x=list(range(len(historia))),
            y=historia,
            mode='lines+markers',
            name=titulo,
            line=dict(color=color, width=2),
            marker=dict(size=4)
        ))

    fig.update_layout(
        title=titulo,
        xaxis_title="Tiempo (muestras)",
        yaxis_title=unidad,
        height=250,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

# ==================== INICIALIZACIÓN DE ESTADO ====================
if 'tanque_sim' not in st.session_state:
    st.session_state.tanque_sim = TanqueSimulado(altura_max=200, diametro=100)
    st.session_state.sensor_us = SensorUltrasonico(altura_instalacion=200)
    st.session_state.sensor_amb = SensorAmbiental()
    st.session_state.simulacion_activa = False
    st.session_state.modo_control = "automatico"  # automatico o manual
    st.session_state.nivel_sim_history = []
    st.session_state.temp_history = []
    st.session_state.presion_history = []
    st.session_state.tiempo_sim = []
    st.session_state.contador_sim = 0
    # Variables para control manual
    st.session_state.nivel_manual = 50.0
    st.session_state.temp_manual = 25.0
    st.session_state.presion_manual = 1013.0

# ==================== HEADER ====================
st.markdown('<p class="main-header">🎮 SCE Gemelo Digital 3D - CONTROL TOTAL INTERACTIVO</p>', unsafe_allow_html=True)
st.markdown("**Sistema de Monitoreo y Control con Interactividad Completa**")

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.info("✨ **NUEVO:** Controla directamente el nivel del tanque, temperatura, presión y todos los parámetros en tiempo real")
with col2:
    st.success("🎛️ Modo Interactivo: Cambia cualquier valor y observa la respuesta inmediata del sistema")
with col3:
    if st.button("📖 Ayuda"):
        st.session_state.show_help = not st.session_state.get('show_help', False)

if st.session_state.get('show_help', False):
    with st.expander("ℹ️ Guía Rápida", expanded=True):
        st.markdown("""
        ### 🎯 Cómo Usar Este Dashboard

        **Modo Manual Total:**
        1. Selecciona "🎮 Control Manual Total" en el sidebar
        2. Usa los sliders para cambiar:
           - 💧 Nivel del tanque directamente
           - 🌡️ Temperatura ambiente
           - 🔽 Presión barométrica
           - Y todos los demás parámetros
        3. Observa los cambios inmediatos en el tanque 3D

        **Modo Simulación Física:**
        1. Selecciona "🔄 Simulación Física"
        2. Configura caudales y umbrales
        3. Presiona ▶️ Iniciar
        4. El sistema evoluciona según las leyes físicas

        **Escenarios Rápidos:**
        - Usa los botones de escenarios predefinidos
        - Experimenta con diferentes situaciones
        """)

st.markdown("---")

# ==================== SIDEBAR - CONTROLES ====================
st.sidebar.title("🎛️ Panel de Control Total")

# Selector de modo
modo_operacion = st.sidebar.radio(
    "🎮 Modo de Operación",
    ["📊 Visualización Datos", "🔄 Simulación Física", "🎮 Control Manual Total"],
    index=2
)

st.sidebar.markdown("---")

# ==================== CONTROLES SEGÚN MODO ====================

if modo_operacion == "🎮 Control Manual Total":
    st.session_state.modo_control = "manual"
    st.session_state.simulacion_activa = False

    st.sidebar.markdown("### 🎯 CONTROL DIRECTO DE TODO")

    # Sección: Nivel del Tanque
    st.sidebar.markdown("#### 💧 Nivel del Tanque")
    altura_max = st.sidebar.slider("Altura Máxima del Tanque (cm)", 100, 300, 200, 10, key="altura_max_manual")

    # Obtener valor inicial para el nivel
    nivel_inicial = float(st.session_state.get('nivel_manual', 50.0))
    if nivel_inicial > altura_max:
        nivel_inicial = float(altura_max) / 2.0

    st.session_state.nivel_manual = st.sidebar.slider(
        "**🎯 NIVEL ACTUAL (cm)**",
        0.0,
        float(altura_max),
        nivel_inicial,
        1.0,
        help="¡Cambia el nivel directamente!",
        key="nivel_slider"
    )

    # Mostrar porcentaje
    porcentaje_nivel = (float(st.session_state.nivel_manual) / float(altura_max)) * 100
    st.sidebar.progress(min(1.0, max(0.0, porcentaje_nivel / 100)))
    st.sidebar.caption(f"Capacidad: {porcentaje_nivel:.1f}%")

    st.sidebar.markdown("---")

    # Sección: Sensores Ambientales
    st.sidebar.markdown("#### 🌡️ Condiciones Ambientales")

    st.session_state.temp_manual = st.sidebar.slider(
        "🌡️ Temperatura (°C)",
        -10.0,
        50.0,
        float(st.session_state.get('temp_manual', 25.0)),
        0.5,
        help="Temperatura ambiente"
    )

    st.session_state.presion_manual = st.sidebar.slider(
        "🔽 Presión Barométrica (hPa)",
        950.0,
        1050.0,
        float(st.session_state.get('presion_manual', 1013.0)),
        1.0,
        help="Presión atmosférica"
    )

    st.sidebar.markdown("---")

    # Sección: Parámetros del Tanque
    st.sidebar.markdown("#### ⚙️ Geometría del Tanque")

    diametro = st.sidebar.slider("Diámetro (cm)", 50, 200, 100, 10, key="diam_manual")

    st.sidebar.markdown("---")

    # Sección: Umbrales
    st.sidebar.markdown("#### ⚠️ Umbrales de Alarma")

    # Ajustar rangos dinámicamente según altura_max
    umbral_bajo_max = min(100, int(altura_max * 0.5))
    umbral_bajo = st.sidebar.slider("Umbral Bajo (cm)", 10, umbral_bajo_max, min(30, umbral_bajo_max), 5, key="umb_bajo_manual")

    # Asegurar que el slider del umbral alto tenga un rango válido
    umbral_alto_min = min(100, int(altura_max * 0.5))
    umbral_alto_max = int(altura_max)

    # Si min >= max, ajustar
    if umbral_alto_min >= umbral_alto_max:
        umbral_alto_min = int(altura_max * 0.4)

    umbral_alto_actual = st.session_state.get('umb_alto_manual', min(170, umbral_alto_max))
    if umbral_alto_actual > umbral_alto_max:
        umbral_alto_actual = umbral_alto_max
    if umbral_alto_actual < umbral_alto_min:
        umbral_alto_actual = umbral_alto_min

    umbral_alto = st.sidebar.slider("Umbral Alto (cm)", umbral_alto_min, umbral_alto_max, umbral_alto_actual, 5, key="umb_alto_manual")

    st.sidebar.markdown("---")

    # Escenarios predefinidos
    st.sidebar.markdown("#### 🎬 Escenarios Rápidos")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🟢 Nivel Normal", use_container_width=True):
            st.session_state.nivel_manual = 100.0
            st.session_state.temp_manual = 25.0
            st.session_state.presion_manual = 1013.0

    with col2:
        if st.button("🔴 Nivel Crítico Alto", use_container_width=True):
            st.session_state.nivel_manual = 180.0
            st.session_state.temp_manual = 30.0

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🟡 Nivel Crítico Bajo", use_container_width=True):
            st.session_state.nivel_manual = 20.0
            st.session_state.temp_manual = 20.0

    with col2:
        if st.button("⚪ Tanque Vacío", use_container_width=True):
            st.session_state.nivel_manual = 0.0

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("💧 Tanque Lleno", use_container_width=True):
            st.session_state.nivel_manual = altura_max

    with col2:
        if st.button("🎲 Aleatorio", use_container_width=True):
            st.session_state.nivel_manual = np.random.uniform(10, altura_max - 10)
            st.session_state.temp_manual = np.random.uniform(15, 35)
            st.session_state.presion_manual = np.random.uniform(990, 1030)

    # Actualizar tanque con valores manuales
    st.session_state.tanque_sim.nivel_actual = st.session_state.nivel_manual
    st.session_state.tanque_sim.H_max = altura_max
    st.session_state.tanque_sim.diametro = diametro
    st.session_state.tanque_sim.area = np.pi * (diametro/2)**2

    nivel_actual = st.session_state.nivel_manual
    temp_actual = st.session_state.temp_manual
    presion_actual = st.session_state.presion_manual

elif modo_operacion == "🔄 Simulación Física":
    st.session_state.modo_control = "automatico"

    st.sidebar.markdown("### ⚙️ Parámetros del Tanque")
    altura_max = st.sidebar.slider("Altura Máxima (cm)", 100, 300, 200, 10, key="altura_sim")
    diametro = st.sidebar.slider("Diámetro (cm)", 50, 200, 100, 10, key="diam_sim")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💧 Caudales")

    caudal_entrada = st.sidebar.slider("Caudal Entrada (L/min)", 0.0, 100.0, 10.0, 1.0)
    caudal_salida = st.sidebar.slider("Caudal Salida (L/min)", 0.0, 100.0, 5.0, 1.0)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ Umbrales")

    # Ajustar rangos dinámicamente según altura_max
    umbral_bajo_max = min(100, int(altura_max * 0.5))
    umbral_bajo = st.sidebar.slider("Umbral Bajo (cm)", 10, umbral_bajo_max, min(30, umbral_bajo_max), 5, key="umb_bajo_sim")

    # Asegurar que el slider del umbral alto tenga un rango válido
    umbral_alto_min = min(100, int(altura_max * 0.5))
    umbral_alto_max = int(altura_max)

    # Si min >= max, ajustar
    if umbral_alto_min >= umbral_alto_max:
        umbral_alto_min = int(altura_max * 0.4)

    umbral_alto_actual = st.session_state.get('umb_alto_sim', min(170, umbral_alto_max))
    if umbral_alto_actual > umbral_alto_max:
        umbral_alto_actual = umbral_alto_max
    if umbral_alto_actual < umbral_alto_min:
        umbral_alto_actual = umbral_alto_min

    umbral_alto = st.sidebar.slider("Umbral Alto (cm)", umbral_alto_min, umbral_alto_max, umbral_alto_actual, 5, key="umb_alto_sim")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Control de Válvulas")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        valvula_entrada = st.checkbox("Válvula Entrada", value=True, key="valv_sim")
    with col2:
        bomba_salida = st.checkbox("Bomba Salida", value=False, key="bomba_sim")

    # Actualizar parámetros
    st.session_state.tanque_sim.H_max = altura_max
    st.session_state.tanque_sim.diametro = diametro
    st.session_state.tanque_sim.area = np.pi * (diametro/2)**2
    st.session_state.tanque_sim.Q_in = caudal_entrada
    st.session_state.tanque_sim.Q_out = caudal_salida
    st.session_state.tanque_sim.set_valvula_entrada(valvula_entrada)
    st.session_state.tanque_sim.set_bomba_salida(bomba_salida)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ▶️ Control de Simulación")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("▶️ Iniciar" if not st.session_state.simulacion_activa else "⏸️ Pausar", use_container_width=True):
            st.session_state.simulacion_activa = not st.session_state.simulacion_activa

    with col2:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.tanque_sim.nivel_actual = 50
            st.session_state.nivel_sim_history = []
            st.session_state.temp_history = []
            st.session_state.presion_history = []
            st.session_state.tiempo_sim = []
            st.session_state.contador_sim = 0
            st.session_state.simulacion_activa = False

    velocidad = st.sidebar.slider("⏱️ Velocidad de actualización (s)", 0.1, 2.0, 0.5, 0.1,
                                   help="Tiempo entre actualizaciones. Mayor = menos flickering")

    # Ejecutar simulación si está activa
    if st.session_state.simulacion_activa:
        st.session_state.tanque_sim.actualizar(dt=0.5)
        temp, presion = st.session_state.sensor_amb.leer()
        distancia = st.session_state.sensor_us.medir_distancia(
            st.session_state.tanque_sim.nivel_actual, temp, presion
        )
        nivel_medido = altura_max - distancia

        st.session_state.nivel_sim_history.append(nivel_medido)
        st.session_state.temp_history.append(temp)
        st.session_state.presion_history.append(presion)
        st.session_state.tiempo_sim.append(st.session_state.contador_sim * 0.5)
        st.session_state.contador_sim += 1

        if len(st.session_state.nivel_sim_history) > 100:
            st.session_state.nivel_sim_history.pop(0)
            st.session_state.temp_history.pop(0)
            st.session_state.presion_history.pop(0)
            st.session_state.tiempo_sim.pop(0)

    nivel_actual = st.session_state.tanque_sim.nivel_actual
    temp_actual = st.session_state.temp_history[-1] if st.session_state.temp_history else 25.0
    presion_actual = st.session_state.presion_history[-1] if st.session_state.presion_history else 1013.0

else:  # Modo Visualización
    st.sidebar.markdown("### 📈 Opciones de Visualización")
    n_muestras = st.sidebar.slider("Muestras a mostrar", 50, 1000, 500, 50)
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (2s)", value=False)

    altura_max = 200
    diametro = 100
    umbral_bajo = 30
    umbral_alto = 170

    df = cargar_datos_historicos()
    if not df.empty:
        df = df.tail(n_muestras)
        nivel_actual = df.iloc[-1]['nivel']
        temp_actual = df.iloc[-1]['temperatura']
        presion_actual = df.iloc[-1]['presion']
    else:
        nivel_actual = 50
        temp_actual = 25
        presion_actual = 1013

# ==================== MÉTRICAS PRINCIPALES ====================
st.markdown("### 📊 Métricas en Tiempo Real")

# Determinar estado
if nivel_actual < umbral_bajo:
    estado = "ALERTA_BAJA"
    emoji_estado = "🟡"
elif nivel_actual > umbral_alto:
    estado = "ALERTA_ALTA"
    emoji_estado = "🔴"
else:
    estado = "NORMAL"
    emoji_estado = "✅"

volumen = np.pi * (diametro/2)**2 * nivel_actual / 1000

# Mostrar métricas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💧 Nivel",
        value=f"{nivel_actual:.2f} cm",
        delta=f"{(nivel_actual/altura_max)*100:.1f}%"
    )

with col2:
    st.metric(
        label="🚦 Estado",
        value=f"{emoji_estado} {estado}"
    )

with col3:
    st.metric(
        label="🌡️ Temperatura",
        value=f"{temp_actual:.1f} °C"
    )

with col4:
    st.metric(
        label="🔽 Presión",
        value=f"{presion_actual:.1f} hPa"
    )

with col5:
    st.metric(
        label="💦 Volumen",
        value=f"{volumen:.1f} L"
    )

st.markdown("---")

# ==================== VISUALIZACIONES ====================

tab1, tab2, tab3 = st.tabs(["🌊 Tanque 3D", "📊 Gráficas Tiempo Real", "📈 Análisis"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        # Obtener valores de caudal y válvulas según el modo
        if modo_operacion == "🔄 Simulación Física":
            caudal_in = caudal_entrada if 'caudal_entrada' in locals() else 0
            caudal_out = caudal_salida if 'caudal_salida' in locals() else 0
            valv_in = valvula_entrada if 'valvula_entrada' in locals() else False
            bomb_out = bomba_salida if 'bomba_salida' in locals() else False
        else:
            caudal_in = 0
            caudal_out = 0
            valv_in = False
            bomb_out = False

        # Inicializar placeholder para tanque 3D (solo una vez)
        if 'tanque_3d_placeholder' not in st.session_state:
            st.session_state.tanque_3d_placeholder = st.empty()

        # Crear figura 3D
        fig_3d = crear_tanque_3d(
            nivel_actual, altura_max, diametro, umbral_bajo, umbral_alto,
            caudal_in, caudal_out, valv_in, bomb_out
        )

        # Actualizar en el placeholder para reducir flickering
        st.session_state.tanque_3d_placeholder.plotly_chart(
            fig_3d,
            use_container_width=True,
            key="tanque_3d_main_chart",
            config={'displayModeBar': False, 'staticPlot': False}
        )

    with col2:
        # Inicializar placeholder para gauge (solo una vez)
        if 'gauge_placeholder' not in st.session_state:
            st.session_state.gauge_placeholder = st.empty()

        # Crear y actualizar gauge
        fig_gauge = crear_gauge_nivel(nivel_actual, altura_max)
        st.session_state.gauge_placeholder.plotly_chart(
            fig_gauge,
            use_container_width=True,
            key="gauge_main_chart",
            config={'displayModeBar': False}
        )

        st.markdown("### 📊 Info del Sistema")
        volumen_max = np.pi * (diametro/2)**2 * altura_max / 1000

        st.info(f"""
        **Modo:** {modo_operacion}

        **Volumen:**
        - Actual: {volumen:.2f} L
        - Máximo: {volumen_max:.2f} L
        - Usado: {(volumen/volumen_max)*100:.1f}%

        **Geometría:**
        - Altura: {altura_max} cm
        - Diámetro: {diametro} cm
        - Radio: {diametro/2} cm

        **Umbrales:**
        - Alto: {umbral_alto} cm
        - Bajo: {umbral_bajo} cm
        """)

        if modo_operacion == "🎮 Control Manual Total":
            st.success("🎮 **MODO MANUAL ACTIVO**\nUsa los sliders del sidebar para control total")

with tab2:
    if modo_operacion == "🔄 Simulación Física" and st.session_state.nivel_sim_history:
        # Gráficas de simulación
        col1, col2 = st.columns(2)

        with col1:
            fig = crear_grafica_historia(st.session_state.nivel_sim_history, "📊 Nivel del Tanque", "#1f77b4", "Nivel (cm)")
            fig.add_hline(y=umbral_alto, line_dash="dash", line_color="red")
            fig.add_hline(y=umbral_bajo, line_dash="dash", line_color="orange")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = crear_grafica_historia(st.session_state.temp_history, "🌡️Temperatura", "#ff7f0e", "Temp (°C)")
            st.plotly_chart(fig, use_container_width=True)

        fig = crear_grafica_historia(st.session_state.presion_history, "🔽 Presión Barométrica", "#2ca02c", "Presión (hPa)")
        st.plotly_chart(fig, use_container_width=True)

    elif modo_operacion == "📊 Visualización Datos":
        df = cargar_datos_historicos()
        if not df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['nivel'], mode='lines', name='Nivel'))
            fig.add_hline(y=umbral_alto, line_dash="dash", line_color="red")
            fig.add_hline(y=umbral_bajo, line_dash="dash", line_color="orange")
            fig.update_layout(title="Nivel Histórico", height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos históricos. Ejecuta el SCE primero.")

    else:
        st.info("""
        ### 📊 Panel de Gráficas en Tiempo Real

        **En Modo Manual:**
        - Los valores se actualizan según tus ajustes
        - No hay historial temporal (es control instantáneo)

        **En Modo Simulación:**
        - Las gráficas muestran la evolución temporal
        - Presiona ▶️ Iniciar para ver las gráficas

        **En Modo Visualización:**
        - Se muestran datos históricos de la BD
        """)

with tab3:
    if modo_operacion == "📊 Visualización Datos":
        df = cargar_datos_historicos()
        if not df.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**🌊 Estadísticas Nivel**")
                st.dataframe(df['nivel'].describe(), use_container_width=True)

            with col2:
                st.markdown("**🌡️ Estadísticas Temperatura**")
                st.dataframe(df['temperatura'].describe(), use_container_width=True)

            with col3:
                st.markdown("**🔽 Estadísticas Presión**")
                st.dataframe(df['presion'].describe(), use_container_width=True)
        else:
            st.warning("No hay datos históricos")
    else:
        st.markdown("### 🎯 Análisis del Sistema Actual")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 Estado del Tanque")
            st.write(f"- **Nivel:** {nivel_actual:.2f} cm")
            st.write(f"- **Porcentaje:** {(nivel_actual/altura_max)*100:.1f}%")
            st.write(f"- **Estado:** {estado}")
            st.write(f"- **Volumen:** {volumen:.2f} L")

            if nivel_actual < umbral_bajo:
                st.error("⚠️ Nivel por debajo del umbral mínimo")
            elif nivel_actual > umbral_alto:
                st.error("🔴 Nivel por encima del umbral máximo")
            else:
                st.success("✅ Sistema operando normalmente")

        with col2:
            st.markdown("#### 🌡️ Condiciones Ambientales")
            st.write(f"- **Temperatura:** {temp_actual:.2f} °C")
            st.write(f"- **Presión:** {presion_actual:.2f} hPa")

            # Calcular velocidad del sonido
            v_sonido = 331.3 + 0.606 * temp_actual
            st.write(f"- **Vel. Sonido:** {v_sonido:.2f} m/s")

            st.info(f"💡 **Modo Activo:** {modo_operacion}")

# ==================== FOOTER ====================
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if modo_operacion == "🔄 Simulación Física":
        st.metric("⏱️ Tiempo Sim", f"{st.session_state.contador_sim * 0.5:.1f} s")
    else:
        st.metric("🎮 Modo", modo_operacion.split()[1])

with col2:
    st.metric("📏 Altura Max", f"{altura_max} cm")

with col3:
    st.metric("📐 Diámetro", f"{diametro} cm")

with col4:
    area = np.pi * (diametro/2)**2
    st.metric("📊 Área Base", f"{area:.0f} cm²")

# Auto-refresh
if modo_operacion == "🔄 Simulación Física" and st.session_state.simulacion_activa:
    time.sleep(velocidad)
    st.rerun()

if modo_operacion == "📊 Visualización Datos" and auto_refresh:
    time.sleep(2)
    st.rerun()