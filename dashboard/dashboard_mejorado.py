"""
Dashboard Web Mejorado con Visualización 3D
Interfaz interactiva con controles en tiempo real
"""
import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import time
import os
import sys

# Añadir ruta para importar módulos de ml
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.ml_prediccion import PredictorNivel

# Configuración de página con tema oscuro
st.set_page_config(
    page_title="SCE Gemelo Digital - Dashboard 3D",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalizado para mejorar la interfaz
st.markdown("""
<style>
    /* Estilo general */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Tarjetas de métricas */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }

    /* Títulos */
    h1 {
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: 800;
    }

    h2, h3 {
        color: #1f77b4;
        font-weight: 700;
    }

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }

    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }

    /* Slider */
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* Info boxes */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES ====================

@st.cache_data(ttl=2)
def cargar_datos():
    """Cargar datos desde SQLite con cache"""
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

@st.cache_resource
def cargar_modelo_ml():
    """Cargar el modelo de ML y cachearlo"""
    try:
        predictor = PredictorNivel()
        # Construir la ruta al modelo de forma robusta
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ml', 'modelo_rf.pkl'))
        predictor.cargar_modelo(filename=model_path)
        return predictor
    except FileNotFoundError:
        st.warning("⚠️ Modelo de ML no encontrado. Ejecuta `python ml/ml_prediccion.py` para entrenarlo.")
        return None

def crear_tanque_3d(nivel_actual, nivel_max=200, estado="NORMAL"):
    """
    Crear visualización 3D del tanque cilíndrico
    """
    # Parámetros del tanque
    radio = 50  # cm
    altura_max = nivel_max

    # Colores según estado
    colores_estado = {
        "NORMAL": "#2ecc71",
        "ALERTA_BAJA": "#f39c12",
        "ALERTA_ALTA": "#e74c3c"
    }
    color_liquido = colores_estado.get(estado, "#3498db")

    # Crear cilindro (paredes del tanque)
    theta = np.linspace(0, 2*np.pi, 50)
    z_pared = np.linspace(0, altura_max, 50)
    theta_grid, z_grid = np.meshgrid(theta, z_pared)
    x_pared = radio * np.cos(theta_grid)
    y_pared = radio * np.sin(theta_grid)

    # Crear líquido (cilindro hasta nivel actual)
    z_liquido = np.linspace(0, nivel_actual, 30)
    theta_liq, z_liq = np.meshgrid(theta, z_liquido)
    x_liquido = radio * 0.95 * np.cos(theta_liq)  # Ligeramente más pequeño
    y_liquido = radio * 0.95 * np.sin(theta_liq)

    # Crear figura
    fig = go.Figure()

    # Paredes del tanque (transparente)
    fig.add_trace(go.Surface(
        x=x_pared, y=y_pared, z=z_grid,
        colorscale=[[0, 'rgba(200,200,200,0.3)'], [1, 'rgba(200,200,200,0.3)']],
        showscale=False,
        name='Tanque',
        hoverinfo='skip'
    ))

    # Líquido
    fig.add_trace(go.Surface(
        x=x_liquido, y=y_liquido, z=z_liq,
        colorscale=[[0, color_liquido], [1, color_liquido]],
        showscale=False,
        name=f'Nivel: {nivel_actual:.1f} cm',
        opacity=0.8
    ))

    # Base del tanque
    x_base = radio * np.outer(np.cos(theta), np.ones(2))
    y_base = radio * np.outer(np.sin(theta), np.ones(2))
    z_base = np.zeros_like(x_base)

    fig.add_trace(go.Surface(
        x=x_base, y=y_base, z=z_base,
        colorscale=[[0, 'rgba(100,100,100,0.8)'], [1, 'rgba(100,100,100,0.8)']],
        showscale=False,
        name='Base',
        hoverinfo='skip'
    ))

    # Líneas de nivel (umbrales)
    # Umbral alto (170 cm)
    fig.add_trace(go.Scatter3d(
        x=radio * np.cos(theta),
        y=radio * np.sin(theta),
        z=np.ones_like(theta) * 170,
        mode='lines',
        line=dict(color='red', width=4),
        name='Umbral Alto (170 cm)',
        hoverinfo='text',
        text='Umbral Alto'
    ))

    # Umbral bajo (30 cm)
    fig.add_trace(go.Scatter3d(
        x=radio * np.cos(theta),
        y=radio * np.sin(theta),
        z=np.ones_like(theta) * 30,
        mode='lines',
        line=dict(color='orange', width=4),
        name='Umbral Bajo (30 cm)',
        hoverinfo='text',
        text='Umbral Bajo'
    ))

    # Configuración de la vista
    fig.update_layout(
        title={
            'text': f"🌊 Tanque 3D - Nivel: {nivel_actual:.2f} cm<br><sub>Estado: {estado}</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'}
        },
        scene=dict(
            xaxis=dict(title='X (cm)', backgroundcolor='rgba(230,230,230,0.5)', gridcolor='white'),
            yaxis=dict(title='Y (cm)', backgroundcolor='rgba(230,230,230,0.5)', gridcolor='white'),
            zaxis=dict(title='Altura (cm)', range=[0, altura_max], backgroundcolor='rgba(230,230,230,0.5)', gridcolor='white'),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2),
                center=dict(x=0, y=0, z=0)
            ),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=2)
        ),
        height=600,
        showlegend=True,
        legend=dict(x=0.7, y=0.95, bgcolor='rgba(255,255,255,0.8)'),
        paper_bgcolor='rgba(240,240,240,0.9)',
        plot_bgcolor='rgba(240,240,240,0.9)'
    )

    return fig

def crear_grafica_nivel_tiempo(df, predictor):
    """Gráfica de nivel vs tiempo mejorada con predicciones"""
    fig = go.Figure()

    # Área bajo la curva (datos históricos)
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['nivel'],
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)',
        line=dict(color='#1f77b4', width=3),
        mode='lines',
        name='Nivel Histórico',
        hovertemplate='<b>Nivel:</b> %{y:.2f} cm<br><b>Tiempo:</b> %{x}<extra></extra>'
    ))

    # --- INICIO LÓGICA DE PREDICCIÓN ---
    if predictor and len(df) >= 5:
        # Últimos 5 niveles para la predicción
        ultimos_niveles = df['nivel'].tail(5).tolist()
        
        # Última temperatura y presión
        temp_actual = df.iloc[-1]['temperatura']
        presion_actual = df.iloc[-1]['presion']

        # Predecir los próximos 20 pasos
        predicciones = predictor.predecir_futuro(
            ultimos_datos=ultimos_niveles,
            temp=temp_actual,
            presion=presion_actual,
            pasos=20
        )

        # Crear timestamps futuros para el eje X
        ultimo_timestamp = df['timestamp'].iloc[-1]
        
        # Estimar la frecuencia de los datos a partir de los últimos 10 puntos
        frecuencia_estimada = pd.to_timedelta(np.diff(df['timestamp'].tail(10)).mean())
        
        # Si la frecuencia no es válida (e.g., pocos datos), usar un valor por defecto
        if pd.isna(frecuencia_estimada) or frecuencia_estimada.total_seconds() <= 0:
            frecuencia_estimada = pd.Timedelta(seconds=1)

        timestamps_futuros = pd.date_range(
            start=ultimo_timestamp + frecuencia_estimada,
            periods=20,
            freq=frecuencia_estimada
        )

        # Añadir la línea de predicción
        fig.add_trace(go.Scatter(
            x=timestamps_futuros,
            y=predicciones,
            mode='lines',
            line=dict(color='red', dash='dash', width=3),
            name='Predicción Futura',
            hovertemplate='<b>Predicción:</b> %{y:.2f} cm<br><b>Tiempo:</b> %{x}<extra></extra>'
        ))
    # --- FIN LÓGICA DE PREDICCIÓN ---

    # Umbrales
    fig.add_hline(y=170, line_dash="dash", line_color="red", line_width=2,
                  annotation_text="Umbral Alto", annotation_position="right")
    fig.add_hline(y=30, line_dash="dash", line_color="orange", line_width=2,
                  annotation_text="Umbral Bajo", annotation_position="right")

    # Zona de peligro (arriba de 170)
    fig.add_hrect(y0=170, y1=200, fillcolor="red", opacity=0.1, line_width=0)
    # Zona de peligro (abajo de 30)
    fig.add_hrect(y0=0, y1=30, fillcolor="orange", opacity=0.1, line_width=0)

    fig.update_layout(
        title="📊 Evolución del Nivel en el Tiempo (Histórico y Predicción)",
        xaxis_title="Tiempo",
        yaxis_title="Nivel (cm)",
        hovermode='x unified',
        height=400,
        template='plotly_white',
        showlegend=True
    )

    return fig

def crear_gauges_sensores(temp, presion, nivel):
    """Crear medidores tipo gauge para sensores"""
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=("🌡️ Temperatura", "🔽 Presión", "💧 Nivel")
    )

    # Gauge de Temperatura
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=temp,
        title={'text': "°C"},
        delta={'reference': 25},
        gauge={
            'axis': {'range': [0, 50]},
            'bar': {'color': "#ff7f0e"},
            'steps': [
                {'range': [0, 20], 'color': "lightblue"},
                {'range': [20, 30], 'color': "lightgreen"},
                {'range': [30, 50], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        }
    ), row=1, col=1)

    # Gauge de Presión
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=presion,
        title={'text': "hPa"},
        delta={'reference': 1013},
        gauge={
            'axis': {'range': [900, 1100]},
            'bar': {'color': "#2ca02c"},
            'steps': [
                {'range': [900, 1000], 'color': "lightblue"},
                {'range': [1000, 1030], 'color': "lightgreen"},
                {'range': [1030, 1100], 'color': "lightcoral"}
            ]
        }
    ), row=1, col=2)

    # Gauge de Nivel
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=nivel,
        title={'text': "cm"},
        delta={'reference': 100},
        gauge={
            'axis': {'range': [0, 200]},
            'bar': {'color': "#1f77b4"},
            'steps': [
                {'range': [0, 30], 'color': "orange"},
                {'range': [30, 170], 'color': "lightgreen"},
                {'range': [170, 200], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 170
            }
        }
    ), row=1, col=3)

    fig.update_layout(
        height=300,
        showlegend=False,
        paper_bgcolor='rgba(240,240,240,0.9)'
    )

    return fig

def crear_mapa_calor_estados(df):
    """Mapa de calor de estados a lo largo del tiempo"""
    # Mapear estados a números
    estado_map = {'NORMAL': 0, 'ALERTA_BAJA': 1, 'ALERTA_ALTA': 2}
    df_temp = df.copy()
    df_temp['estado_num'] = df_temp['estado'].map(estado_map)

    # Agrupar por intervalos de tiempo
    df_temp['time_group'] = pd.cut(range(len(df_temp)), bins=20)

    fig = go.Figure(data=go.Heatmap(
        z=[df_temp['estado_num'].values],
        x=df_temp['timestamp'],
        colorscale=[
            [0, '#2ecc71'],    # Verde - NORMAL
            [0.5, '#f39c12'],  # Naranja - ALERTA_BAJA
            [1, '#e74c3c']     # Rojo - ALERTA_ALTA
        ],
        showscale=True,
        colorbar=dict(
            title="Estado",
            tickvals=[0, 1, 2],
            ticktext=['NORMAL', 'ALERTA_BAJA', 'ALERTA_ALTA']
        )
    ))

    fig.update_layout(
        title="🗺️ Mapa de Calor de Estados del Sistema",
        xaxis_title="Tiempo",
        yaxis_title="",
        height=150,
        yaxis=dict(showticklabels=False)
    )

    return fig

# ==================== INTERFAZ PRINCIPAL ====================

# Header con logo y título
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown("# 🌊")
with col_title:
    st.markdown("# Sistema de Monitoreo de Nivel - Dashboard 3D Interactivo")

# Mensaje de información del proyecto
with st.expander("📚 Información del Proyecto", expanded=False):
    st.markdown("""
    ### Evaluación 3 - Microprocesadores Aplicados a Control

    **Sistema Computacional Empotrado (SCE)** implementado con:
    - ✅ Programación Orientada a Objetos (POO)
    - ✅ Planificador Ejecutivo Cíclico (Tiempo Real)
    - ✅ Fusión de Datos Multisensor
    - ✅ Machine Learning con Random Forest
    - ✅ Dashboard 3D Interactivo

    ---

    **👥 Desarrollado por:**
    - Ing. Torres Rousemery
    - Ing. Pinto Adrian
    - Ing. Cova Luis

    **🎓 Universidad de Oriente - Núcleo Anzoátegui**
    Postgrado en Ingeniería Eléctrica
    Especialización en Automatización e Informática Industrial

    *Diciembre 2024*
    """)

st.markdown("---")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Panel de Control")

    # Modo de visualización
    modo = st.radio(
        "🎨 Modo de Vista",
        ["Dashboard Completo", "Vista 3D", "Análisis Detallado", "Control Manual"],
        help="Selecciona el modo de visualización"
    )

    st.markdown("---")

    # Controles de parámetros
    st.markdown("### 🎛️ Parámetros del Sistema")

    with st.expander("⚡ Parámetros de Simulación", expanded=True):
        caudal_entrada = st.slider(
            "💧 Caudal de Entrada (L/min)",
            min_value=0.0,
            max_value=10.0,
            value=5.0,
            step=0.5,
            help="Ajusta el caudal de entrada al tanque"
        )

        caudal_salida = st.slider(
            "🚰 Caudal de Salida (L/min)",
            min_value=0.0,
            max_value=10.0,
            value=3.0,
            step=0.5,
            help="Ajusta el caudal de salida del tanque"
        )

    with st.expander("⚠️ Umbrales de Alarma"):
        umbral_alto = st.slider(
            "🔴 Umbral Alto (cm)",
            min_value=100,
            max_value=190,
            value=170,
            step=5
        )

        umbral_bajo = st.slider(
            "🟡 Umbral Bajo (cm)",
            min_value=10,
            max_value=100,
            value=30,
            step=5
        )

    st.markdown("---")

    # Configuración de actualización
    st.markdown("### 🔄 Actualización")
    auto_refresh = st.checkbox("Auto-refresh (cada 2s)", value=False)
    n_muestras = st.slider("📊 Muestras", 50, 1000, 500, 50)

    if st.button("🔄 Actualizar Datos Ahora"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")

    # Información del sistema
    st.markdown("### 📘 Acerca del Sistema")
    st.info("""
    **Dashboard 3D Mejorado**

    Características:
    - Visualización 3D del tanque
    - Controles interactivos
    - Gauges en tiempo real
    - Mapa de calor de estados
    - Análisis predictivo

    **Equipo UDO**
    Torres | Pinto | Cova
    """)

# ==================== CARGA DE DATOS Y MODELO ====================
df = cargar_datos()
predictor_ml = cargar_modelo_ml()  # Cargar modelo de ML

if df.empty:
    st.error("⚠️ **No hay datos disponibles**")
    st.info("💡 Ejecuta primero: `python sce/sce_gemelo_digital.py`")
    st.stop()

# Filtrar datos
df = df.tail(n_muestras)

# Datos actuales
ultimo_nivel = df.iloc[-1]['nivel']
ultimo_estado = df.iloc[-1]['estado']
temp_actual = df.iloc[-1]['temperatura']
presion_actual = df.iloc[-1]['presion']

# Calcular delta
if len(df) >= 10:
    delta_nivel = ultimo_nivel - df.iloc[-10]['nivel']
else:
    delta_nivel = 0

# ==================== CONTENIDO PRINCIPAL ====================

if modo == "Dashboard Completo":
    # KPIs principales
    st.markdown("### 📊 Indicadores en Tiempo Real")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        emoji_nivel = "🟢" if 30 < ultimo_nivel < 170 else ("🔴" if ultimo_nivel >= 170 else "🟡")
        st.metric(
            label=f"{emoji_nivel} Nivel Actual",
            value=f"{ultimo_nivel:.2f} cm",
            delta=f"{delta_nivel:+.2f} cm"
        )

    with col2:
        emoji_estado = {'NORMAL': '✅', 'ALERTA_BAJA': '🟡', 'ALERTA_ALTA': '🔴'}.get(ultimo_estado, '⚪')
        st.metric(
            label=f"{emoji_estado} Estado",
            value=ultimo_estado
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

    st.markdown("---")

    # Visualización principal: 3D + Gráfica de tiempo
    col_3d, col_graph = st.columns([1, 1])

    with col_3d:
        st.plotly_chart(
            crear_tanque_3d(ultimo_nivel, 200, ultimo_estado),
            use_container_width=True,
            key="tanque3d_main"
        )

    with col_graph:
        st.plotly_chart(
            crear_grafica_nivel_tiempo(df, predictor_ml),
            use_container_width=True
        )

    # Gauges de sensores
    st.plotly_chart(
        crear_gauges_sensores(temp_actual, presion_actual, ultimo_nivel),
        use_container_width=True
    )

    # Mapa de calor
    st.plotly_chart(
        crear_mapa_calor_estados(df),
        use_container_width=True
    )

elif modo == "Vista 3D":
    # Vista 3D grande
    st.markdown("### 🎮 Vista 3D del Tanque")

    col1, col2 = st.columns([3, 1])

    with col1:
        fig_3d = crear_tanque_3d(ultimo_nivel, 200, ultimo_estado)
        fig_3d.update_layout(height=700)
        st.plotly_chart(fig_3d, use_container_width=True, key="tanque3d_large")

    with col2:
        st.markdown("#### 📈 Estadísticas")
        st.metric("Nivel Actual", f"{ultimo_nivel:.2f} cm")
        st.metric("Estado", ultimo_estado)
        st.metric("Temperatura", f"{temp_actual:.1f} °C")
        st.metric("Presión", f"{presion_actual:.1f} hPa")

        st.markdown("---")
        st.markdown("#### ⚙️ Parámetros")
        st.write(f"💧 Q entrada: {caudal_entrada} L/min")
        st.write(f"🚰 Q salida: {caudal_salida} L/min")
        st.write(f"🔴 Umbral alto: {umbral_alto} cm")
        st.write(f"🟡 Umbral bajo: {umbral_bajo} cm")

elif modo == "Análisis Detallado":
    # Análisis con múltiples gráficas
    st.markdown("### 📊 Análisis Detallado del Sistema")

    tabs = st.tabs(["📈 Nivel", "🌡️ Sensores", "📊 Estadísticas", "🗺️ Mapas"])

    with tabs[0]:
        st.plotly_chart(crear_grafica_nivel_tiempo(df), use_container_width=True)

        # Estadísticas de nivel
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nivel Promedio", f"{df['nivel'].mean():.2f} cm")
        with col2:
            st.metric("Nivel Máximo", f"{df['nivel'].max():.2f} cm")
        with col3:
            st.metric("Nivel Mínimo", f"{df['nivel'].min():.2f} cm")

    with tabs[1]:
        st.plotly_chart(crear_gauges_sensores(temp_actual, presion_actual, ultimo_nivel),
                       use_container_width=True)

        # Gráficas de sensores
        fig_sensores = make_subplots(rows=2, cols=1,
                                     subplot_titles=("Temperatura", "Presión"))

        fig_sensores.add_trace(go.Scatter(x=df['timestamp'], y=df['temperatura'],
                                         name='Temperatura', line=dict(color='#ff7f0e')),
                              row=1, col=1)

        fig_sensores.add_trace(go.Scatter(x=df['timestamp'], y=df['presion'],
                                         name='Presión', line=dict(color='#2ca02c')),
                              row=2, col=1)

        fig_sensores.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_sensores, use_container_width=True)

    with tabs[2]:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 Estadísticas de Nivel")
            st.dataframe(df['nivel'].describe().to_frame(), use_container_width=True)

        with col2:
            st.markdown("#### 🌡️ Estadísticas de Temperatura")
            st.dataframe(df['temperatura'].describe().to_frame(), use_container_width=True)

        # Distribución de estados
        estados_count = df['estado'].value_counts()
        fig_estados = go.Figure(data=[go.Pie(
            labels=estados_count.index,
            values=estados_count.values,
            hole=.3,
            marker_colors=['#2ecc71', '#f39c12', '#e74c3c']
        )])
        fig_estados.update_layout(title="Distribución de Estados", height=400)
        st.plotly_chart(fig_estados, use_container_width=True)

    with tabs[3]:
        st.plotly_chart(crear_mapa_calor_estados(df), use_container_width=True)

        # Tabla de últimas mediciones
        st.markdown("#### 📋 Últimas Mediciones")
        df_display = df[['timestamp', 'nivel', 'temperatura', 'presion', 'estado']].tail(20).copy()
        df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df_display.columns = ['Fecha/Hora', 'Nivel (cm)', 'Temp (°C)', 'Presión (hPa)', 'Estado']
        st.dataframe(df_display.sort_values('Fecha/Hora', ascending=False),
                    use_container_width=True, hide_index=True)

elif modo == "Control Manual":
    st.markdown("### 🎛️ Panel de Control Manual")

    st.warning("""
    ⚠️ **Modo de Control Manual**

    En este modo puedes ajustar los parámetros del sistema en tiempo real.
    Los cambios se aplicarían a una simulación en vivo (no implementado en esta versión).
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💧 Control de Flujos")

        valvula_entrada = st.toggle("Válvula de Entrada", value=True)
        st.write(f"Estado: {'🟢 ABIERTA' if valvula_entrada else '🔴 CERRADA'}")

        if valvula_entrada:
            q_in = st.number_input("Caudal (L/min)", 0.0, 10.0, caudal_entrada, 0.5)

        st.markdown("---")

        bomba_salida = st.toggle("Bomba de Salida", value=False)
        st.write(f"Estado: {'🟢 ENCENDIDA' if bomba_salida else '🔴 APAGADA'}")

        if bomba_salida:
            q_out = st.number_input("Caudal Salida (L/min)", 0.0, 10.0, caudal_salida, 0.5, key="q_out")

    with col2:
        st.markdown("#### 📊 Visualización Actual")
        fig_3d_control = crear_tanque_3d(ultimo_nivel, 200, ultimo_estado)
        fig_3d_control.update_layout(height=500)
        st.plotly_chart(fig_3d_control, use_container_width=True, key="tanque3d_control")

    st.markdown("---")

    # Botones de acción
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

    with col_btn1:
        if st.button("🔄 Resetear Sistema", use_container_width=True):
            st.success("Sistema reseteado")

    with col_btn2:
        if st.button("⏸️ Pausar", use_container_width=True):
            st.info("Sistema pausado")

    with col_btn3:
        if st.button("▶️ Reanudar", use_container_width=True):
            st.success("Sistema reanudado")

    with col_btn4:
        if st.button("💾 Guardar Config", use_container_width=True):
            st.success("Configuración guardada")

# ==================== FOOTER ====================
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 Total Registros", len(df))

with col2:
    duracion = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()
    st.metric("⏱️ Duración", f"{duracion/60:.1f} min")

with col3:
    ultima_act = df['timestamp'].max().strftime('%H:%M:%S')
    st.metric("🕐 Última Actualización", ultima_act)

# Auto-refresh
if auto_refresh:
    time.sleep(2)
    st.rerun()
