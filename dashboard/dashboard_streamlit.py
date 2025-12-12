"""
Dashboard Web Interactivo con Streamlit
Visualización en tiempo real del Gemelo Digital
"""
import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import os

# Configuración de página
st.set_page_config(
    page_title="SCE - Gemelo Digital",
    page_icon="🌊",
    layout="wide"
)

# ==================== FUNCIONES ====================
@st.cache_data(ttl=2)
def cargar_datos():
    """Cargar datos desde SQLite con cache"""
    # Usar ruta absoluta basada en el directorio raíz del proyecto
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

def crear_grafica_nivel(df):
    """Gráfica principal de nivel"""
    fig = go.Figure()
    
    # Nivel
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['nivel'],
        mode='lines+markers',
        name='Nivel',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))
    
    # Umbrales
    fig.add_hline(y=170, line_dash="dash", line_color="red", 
                  annotation_text="Umbral Alto (170 cm)")
    fig.add_hline(y=30, line_dash="dash", line_color="orange", 
                  annotation_text="Umbral Bajo (30 cm)")
    
    fig.update_layout(
        title="📊 Nivel del Tanque en Tiempo Real",
        xaxis_title="Tiempo",
        yaxis_title="Nivel (cm)",
        hovermode='x unified',
        height=500
    )
    
    return fig

def crear_grafica_ambiental(df):
    """Gráfica de sensores ambientales"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("🌡️ Temperatura", "🔽 Presión Barométrica"),
        vertical_spacing=0.15
    )
    
    # Temperatura
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'], 
            y=df['temperatura'], 
            name='Temperatura',
            line=dict(color='#ff7f0e', width=2)
        ),
        row=1, col=1
    )
    
    # Presión
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'], 
            y=df['presion'], 
            name='Presión',
            line=dict(color='#2ca02c', width=2)
        ),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Tiempo", row=2, col=1)
    fig.update_yaxes(title_text="°C", row=1, col=1)
    fig.update_yaxes(title_text="hPa", row=2, col=1)
    fig.update_layout(height=600, showlegend=False)
    
    return fig

def crear_histograma_estados(df):
    """Distribución de estados"""
    estados = df['estado'].value_counts()
    
    colores = {
        'NORMAL': '#2ca02c',
        'ALERTA_BAJA': '#ff7f0e',
        'ALERTA_ALTA': '#d62728'
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=estados.index,
            y=estados.values,
            marker_color=[colores.get(e, '#gray') for e in estados.index]
        )
    ])
    
    fig.update_layout(
        title="⚠️ Distribución de Estados",
        xaxis_title="Estado",
        yaxis_title="Frecuencia",
        height=300
    )
    
    return fig

# ==================== INTERFAZ ====================
# Header
st.title("🌊 Sistema de Monitoreo de Nivel - Gemelo Digital")
st.markdown("**Simulación de SCE con Raspberry Pi 3 + Fusión de Datos + Machine Learning**")

# Mensaje de bienvenida personalizado
st.info(
    """
    **📚 Evaluación 3 - Microprocesadores Aplicados a Control**

    Sistema Computacional Empotrado (SCE) implementado con:
    ✅ Programación Orientada a Objetos (POO)
    ✅ Planificador Ejecutivo Cíclico (Tiempo Real)
    ✅ Fusión de Datos Multisensor
    ✅ Machine Learning con Random Forest
    ✅ Dashboard Interactivo Web

    ---

    **👥 Desarrollado por:**
    - Ing. Torres Rousemery
    - Ing. Pinto Adrian
    - Ing. Cova Luis

    **🎓 Universidad de Oriente - Núcleo Anzoátegui**
    Postgrado en Ingeniería Eléctrica
    Especialización en Automatización e Informática Industrial

    *Diciembre 2024*
    """
)

st.markdown("---")

# Sidebar
st.sidebar.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=SCE+UDO", use_container_width=True)
st.sidebar.header("⚙️ Configuración")
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (cada 2s)", value=False)
n_muestras = st.sidebar.slider("📊 Muestras a mostrar", 50, 1000, 500, 50)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📘 Acerca del Proyecto")
st.sidebar.info(
    """
    **Evaluación 3**
    Microprocesadores Aplicados a Control

    **👥 Equipo de Desarrollo:**
    - Ing. Torres Rousemery
    - Ing. Pinto Adrian
    - Ing. Cova Luis

    **🎓 Institución:**
    Universidad de Oriente
    Núcleo Anzoátegui
    Postgrado en Ingeniería Eléctrica

    **📅 Fecha:** Diciembre 2024
    """
)

# Cargar datos
df = cargar_datos()

if df.empty:
    st.warning("⚠️ **No hay datos disponibles**")
    st.info("💡 Ejecute primero: `python sce/sce_gemelo_digital.py -t 300`")
    st.stop()

# Filtrar por número de muestras
df = df.tail(n_muestras)

# ==================== KPIs ====================
st.subheader("📌 Indicadores en Tiempo Real")

col1, col2, col3, col4 = st.columns(4)

ultimo_nivel = df.iloc[-1]['nivel']
ultimo_estado = df.iloc[-1]['estado']
temp_actual = df.iloc[-1]['temperatura']
presion_actual = df.iloc[-1]['presion']

# Calcular delta (cambio respecto a hace 10 muestras)
if len(df) >= 10:
    delta_nivel = ultimo_nivel - df.iloc[-10]['nivel']
else:
    delta_nivel = 0

# KPI 1: Nivel
with col1:
    st.metric(
        label="💧 Nivel Actual",
        value=f"{ultimo_nivel:.2f} cm",
        delta=f"{delta_nivel:+.2f} cm"
    )

# KPI 2: Estado
with col2:
    emoji_estado = {
        'NORMAL': '✅',
        'ALERTA_BAJA': '🟡',
        'ALERTA_ALTA': '🔴'
    }
    st.metric(
        label="🚦 Estado",
        value=f"{emoji_estado.get(ultimo_estado, '⚪')} {ultimo_estado}"
    )

# KPI 3: Temperatura
with col3:
    st.metric(
        label="🌡️ Temperatura",
        value=f"{temp_actual:.1f} °C"
    )

# KPI 4: Presión
with col4:
    st.metric(
        label="🔽 Presión",
        value=f"{presion_actual:.1f} hPa"
    )

st.markdown("---")

# ==================== GRÁFICAS ====================
# Nivel del tanque
st.plotly_chart(crear_grafica_nivel(df), use_container_width=True)

# Columnas para sensores ambientales y distribución de estados
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(crear_grafica_ambiental(df), use_container_width=True)

with col2:
    st.plotly_chart(crear_histograma_estados(df), use_container_width=True)

# ==================== ESTADÍSTICAS ====================
st.markdown("---")
st.subheader("📈 Estadísticas del Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🌊 Nivel**")
    st.dataframe(df['nivel'].describe().to_frame(), use_container_width=True)

with col2:
    st.markdown("**🌡️ Temperatura**")
    st.dataframe(df['temperatura'].describe().to_frame(), use_container_width=True)

with col3:
    st.markdown("**🔽 Presión**")
    st.dataframe(df['presion'].describe().to_frame(), use_container_width=True)

# ==================== TABLA DE DATOS ====================
st.markdown("---")
st.subheader("📋 Últimas Mediciones")

# Formatear tabla
df_display = df[['timestamp', 'nivel', 'temperatura', 'presion', 'estado']].tail(20).copy()
df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
df_display.columns = ['Fecha/Hora', 'Nivel (cm)', 'Temp (°C)', 'Presión (hPa)', 'Estado']

st.dataframe(
    df_display.sort_values('Fecha/Hora', ascending=False),
    use_container_width=True,
    hide_index=True
)

# ==================== FOOTER ====================
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 Total de Registros", len(df))

with col2:
    duracion = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()
    st.metric("⏱️ Duración Total", f"{duracion/60:.1f} min")

with col3:
    ultima_actualizacion = df['timestamp'].max().strftime('%H:%M:%S')
    st.metric("🕐 Última Actualización", ultima_actualizacion)

# Auto-refresh
if auto_refresh:
    time.sleep(2)
    st.rerun()
