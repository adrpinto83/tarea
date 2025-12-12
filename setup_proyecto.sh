#!/bin/bash

# Script de configuración automática para Evaluación 3 - SCE Gemelo Digital
# Autor: Equipo Torres, Pinto, Cova
# Fecha: Diciembre 2024

echo "🚀 Iniciando configuración del proyecto SCE Gemelo Digital..."
echo "=================================================="

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Crear estructura de carpetas
echo -e "${BLUE}📁 Creando estructura de carpetas...${NC}"
mkdir -p simuladores
mkdir -p sce
mkdir -p ml
mkdir -p dashboard
mkdir -p datos
mkdir -p resultados/graficas_dashboard
mkdir -p resultados/capturas_video
mkdir -p documentos

# Crear archivos __init__.py
touch simuladores/__init__.py
touch sce/__init__.py
touch ml/__init__.py

echo -e "${GREEN}✓ Estructura de carpetas creada${NC}"

# ==================== SIMULADOR DEL TANQUE ====================
echo -e "${BLUE}📝 Creando simulador_tanque.py...${NC}"
cat > simuladores/simulador_tanque.py << 'EOF'
"""
Simulador del Sistema Físico - Tanque con Sensores
Autor: Equipo SCE
"""
import numpy as np
import time
from datetime import datetime

class TanqueSimulado:
    """
    Simula la dinámica de un tanque con entrada/salida
    Ecuación diferencial: dh/dt = (Q_in - Q_out) / Area
    """
    def __init__(self, altura_max=200, diametro=100, caudal_entrada=5, caudal_salida=3):
        self.H_max = altura_max  # cm
        self.diametro = diametro  # cm
        self.area = np.pi * (diametro/2)**2  # cm²
        self.nivel_actual = 50  # cm (nivel inicial)
        self.Q_in = caudal_entrada  # L/min
        self.Q_out = caudal_salida  # L/min
        self.valvula_entrada = True
        self.bomba_salida = False
        
    def actualizar(self, dt=1.0):
        """
        Actualiza nivel según ecuación diferencial
        dt en segundos
        """
        # Convertir caudales a cm³/s
        q_in = (self.Q_in * 1000 / 60) if self.valvula_entrada else 0  # cm³/s
        q_out = (self.Q_out * 1000 / 60) if self.bomba_salida else 0  # cm³/s
        
        # dh/dt = (Q_in - Q_out) / Area
        dh = ((q_in - q_out) / self.area) * dt
        self.nivel_actual += dh
        
        # Límites físicos
        self.nivel_actual = np.clip(self.nivel_actual, 0, self.H_max)
        
        return self.nivel_actual
    
    def set_valvula_entrada(self, estado):
        """Abrir/cerrar válvula de entrada"""
        self.valvula_entrada = estado
    
    def set_bomba_salida(self, estado):
        """Encender/apagar bomba de salida"""
        self.bomba_salida = estado

class SensorUltrasonico:
    """
    Simula sensor JSN-SR04T con ruido y errores
    """
    def __init__(self, altura_instalacion=200):
        self.H = altura_instalacion  # Altura donde está instalado (cm)
        self.error_std = 0.5  # Desviación estándar del ruido (cm)
        
    def medir_distancia(self, nivel_real, temperatura=20, presion=1013):
        """
        Simula medición con ToF (Time of Flight)
        Incluye corrección por temperatura y ruido
        """
        distancia_real = self.H - nivel_real
        
        # Simulación de velocidad del sonido corregida por temperatura
        v_sonido = 331.3 + 0.606 * temperatura  # m/s
        
        # ToF = 2*d/v (ida y vuelta)
        tof_teorico = (2 * distancia_real / 100) / v_sonido  # segundos
        
        # Agregar ruido gaussiano
        ruido = np.random.normal(0, self.error_std)
        distancia_medida = distancia_real + ruido
        
        # Lecturas erráticas ocasionales (5% probabilidad)
        if np.random.random() < 0.05:
            distancia_medida += np.random.uniform(-10, 10)
        
        # Simular delay del sensor (40 kHz, ~25ms típico)
        time.sleep(0.001)  # 1ms
            
        return max(0, min(distancia_medida, self.H))

class SensorAmbiental:
    """
    Simula sensor BME280 (temperatura y presión)
    """
    def __init__(self):
        self.temp_base = 25.0  # °C
        self.presion_base = 1013.0  # hPa
        self.drift_temp = 0  # Deriva lenta de temperatura
        
    def leer(self):
        """
        Simula lecturas con variaciones pequeñas + deriva lenta
        """
        # Deriva lenta (simulación de cambio ambiental)
        self.drift_temp += np.random.normal(0, 0.01)
        
        temp = self.temp_base + self.drift_temp + np.random.normal(0, 0.3)
        presion = self.presion_base + np.random.normal(0, 1.5)
        
        return temp, presion

# ==================== PRUEBA RÁPIDA ====================
if __name__ == "__main__":
    print("🧪 Prueba del simulador...")
    
    tanque = TanqueSimulado(altura_max=200, diametro=100)
    sensor_us = SensorUltrasonico(altura_instalacion=200)
    sensor_amb = SensorAmbiental()
    
    print(f"Nivel inicial: {tanque.nivel_actual:.2f} cm")
    
    for i in range(20):
        tanque.actualizar(dt=1.0)
        temp, presion = sensor_amb.leer()
        distancia = sensor_us.medir_distancia(tanque.nivel_actual, temp, presion)
        nivel_calculado = 200 - distancia
        
        print(f"t={i+1}s | Nivel real: {tanque.nivel_actual:.2f} | "
              f"Medido: {nivel_calculado:.2f} | Temp: {temp:.1f}°C")
    
    print("✅ Simulador funcionando correctamente")
EOF

echo -e "${GREEN}✓ simulador_tanque.py creado${NC}"

# ==================== SCE GEMELO DIGITAL ====================
echo -e "${BLUE}📝 Creando sce_gemelo_digital.py...${NC}"
cat > sce/sce_gemelo_digital.py << 'EOF'
"""
Sistema Computacional Empotrado - Gemelo Digital
Implementación con POO y Planificador Ejecutivo Cíclico
"""
import sys
sys.path.append('..')

import numpy as np
from simuladores.simulador_tanque import TanqueSimulado, SensorUltrasonico, SensorAmbiental
import sqlite3
from datetime import datetime
import time

# ==================== CLASES POO (De Tarea 2) ====================
class SensorBase:
    """Clase base para todos los sensores"""
    def __init__(self, id_sensor, pin_gpio=None):
        self.ID_Sensor = id_sensor
        self.Pin_GPIO = pin_gpio
        self.Estado_HW = "OK"
    
    def inicializar(self):
        print(f"[{self.ID_Sensor}] Inicializado (simulado)")
    
    def obtener_dato_crudo(self):
        raise NotImplementedError("Método debe ser implementado por subclase")

class SensorUltrasonicoSCE(SensorBase):
    """Sensor Ultrasónico JSN-SR04T"""
    def __init__(self, id_sensor, sensor_simulado):
        super().__init__(id_sensor, pin_gpio=23)
        self.sensor_sim = sensor_simulado
        self.TOF = 0
        self.Distancia_Cruda = 0
        
    def emitir_pulso(self):
        """Simulado - en hardware real enviaría pulso de 10μs"""
        pass
    
    def medir_TOF(self, nivel_tanque, temp, presion):
        """Mide tiempo de vuelo y calcula distancia"""
        self.Distancia_Cruda = self.sensor_sim.medir_distancia(nivel_tanque, temp, presion)
        return self.Distancia_Cruda

class SensorAmbientalSCE(SensorBase):
    """Sensor Ambiental BME280 (I2C)"""
    def __init__(self, id_sensor, sensor_simulado):
        super().__init__(id_sensor, pin_gpio=2)  # GPIO2 = SDA
        self.sensor_sim = sensor_simulado
        self.Temperatura = 0
        self.Presion_Barometrica = 0
        
    def leer_T(self):
        """Lee temperatura"""
        self.Temperatura, self.Presion_Barometrica = self.sensor_sim.leer()
        return self.Temperatura
    
    def leer_P(self):
        """Lee presión barométrica"""
        return self.Presion_Barometrica

class FusionadorDatos:
    """
    Fusión de datos multisensor con filtrado digital
    """
    def __init__(self):
        self.Peso_T = 0.6
        self.Peso_P = 0.4
        self.Lecturas_Historicas = []
        self.ventana_filtro = 5
        
    def calcular_v_sonido_corregida(self, T, P):
        """
        Velocidad del sonido corregida por temperatura y presión
        v = 331.3 + 0.606*T [m/s]
        """
        v = 331.3 + 0.606 * T
        # Corrección por presión (simplificada)
        factor_p = 1 + (P - 1013) * 0.0001
        return v * factor_p
    
    def ejecutar_fusion(self, d_cruda, T, P, H_tanque):
        """
        Fusión de datos con filtrado de promedio móvil
        """
        v_corregida = self.calcular_v_sonido_corregida(T, P)
        
        # Calcular nivel
        nivel = H_tanque - d_cruda
        
        # Filtro de promedio móvil
        self.Lecturas_Historicas.append(nivel)
        if len(self.Lecturas_Historicas) > self.ventana_filtro:
            self.Lecturas_Historicas.pop(0)
        
        nivel_filtrado = np.mean(self.Lecturas_Historicas)
        return nivel_filtrado

class ControladorNivel:
    """
    Controlador con lógica de alarmas e histéresis
    """
    def __init__(self, H_max, umbral_bajo=20, umbral_alto=180):
        self.Nivel_Actual = 0
        self.H_Max = H_max
        self.Umbral_Bajo = umbral_bajo
        self.Umbral_Alto = umbral_alto
        self.Estado_Alarma = "NORMAL"
        self.histeresis = 5  # cm
        
    def procesar_lectura(self, nivel_fusionado):
        """Actualiza nivel actual"""
        self.Nivel_Actual = nivel_fusionado
        
    def ejecutar_logica_control(self):
        """
        Lógica de control con histéresis
        """
        if self.Nivel_Actual <= self.Umbral_Bajo:
            self.Estado_Alarma = "ALERTA_BAJA"
            return "ACTIVAR_ENTRADA"
        elif self.Nivel_Actual >= self.Umbral_Alto:
            self.Estado_Alarma = "ALERTA_ALTA"
            return "ACTIVAR_SALIDA"
        else:
            # Zona de histéresis
            if self.Estado_Alarma == "ALERTA_BAJA" and self.Nivel_Actual < self.Umbral_Bajo + self.histeresis:
                return "ACTIVAR_ENTRADA"
            elif self.Estado_Alarma == "ALERTA_ALTA" and self.Nivel_Actual > self.Umbral_Alto - self.histeresis:
                return "ACTIVAR_SALIDA"
            else:
                self.Estado_Alarma = "NORMAL"
                return "MANTENER"
    
    def activar_alarma(self):
        """Muestra alarma si hay problema"""
        if self.Estado_Alarma != "NORMAL":
            print(f"⚠️  ALARMA: {self.Estado_Alarma} - Nivel: {self.Nivel_Actual:.2f} cm")

# ==================== BASE DE DATOS ====================
class AlmacenamientoLocal:
    """Almacenamiento en SQLite"""
    def __init__(self, db_file="../datos/datos_sce.db"):
        self.conn = sqlite3.connect(db_file)
        self.crear_tabla()
    
    def crear_tabla(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mediciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                nivel REAL,
                temperatura REAL,
                presion REAL,
                estado TEXT
            )
        """)
        self.conn.commit()
    
    def guardar(self, nivel, temp, presion, estado):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO mediciones (timestamp, nivel, temperatura, presion, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), nivel, temp, presion, estado))
        self.conn.commit()
    
    def cerrar(self):
        self.conn.close()

# ==================== PLANIFICADOR EJECUTIVO CÍCLICO ====================
class PlanificadorCiclico:
    """
    Planificador Ejecutivo Cíclico
    T_menor = 100ms
    T_mayor = 2000ms (MCM de todos los períodos)
    """
    def __init__(self):
        self.T_menor = 0.1  # 100ms
        self.frame_actual = 0
        self.tareas = {
            'T1': {'periodo': 1, 'ultima_ejecucion': 0, 'nombre': 'Adquisición/Fusión'},
            'T2': {'periodo': 2, 'ultima_ejecucion': 0, 'nombre': 'Control'},
            'T3': {'periodo': 10, 'ultima_ejecucion': 0, 'nombre': 'Almacenamiento'},
            'T4': {'periodo': 20, 'ultima_ejecucion': 0, 'nombre': 'Comunicación'},
        }
    
    def ejecutar_frame(self, sistema):
        """Ejecuta tareas según plan cíclico"""
        tareas_ejecutadas = []
        
        # T1: Adquisición y Fusión (cada frame)
        if self.frame_actual % self.tareas['T1']['periodo'] == 0:
            sistema.tarea_adquisicion_fusion()
            tareas_ejecutadas.append('T1')
        
        # T2: Control
        if self.frame_actual % self.tareas['T2']['periodo'] == 0:
            sistema.tarea_control()
            tareas_ejecutadas.append('T2')
        
        # T3: Almacenamiento
        if self.frame_actual % self.tareas['T3']['periodo'] == 0:
            sistema.tarea_almacenamiento()
            tareas_ejecutadas.append('T3')
        
        # T4: Comunicación
        if self.frame_actual % self.tareas['T4']['periodo'] == 0:
            sistema.tarea_comunicacion()
            tareas_ejecutadas.append('T4')
        
        self.frame_actual += 1
        return tareas_ejecutadas

# ==================== SISTEMA INTEGRADO ====================
class SistemaGemeloDigital:
    """Sistema completo: Gemelo Digital del SCE"""
    def __init__(self):
        print("🔧 Inicializando Gemelo Digital...")
        
        # Simuladores físicos
        self.tanque = TanqueSimulado(altura_max=200, diametro=100)
        self.sensor_us_sim = SensorUltrasonico(altura_instalacion=200)
        self.sensor_amb_sim = SensorAmbiental()
        
        # SCE (POO)
        self.sensor_us = SensorUltrasonicoSCE("US-01", self.sensor_us_sim)
        self.sensor_amb = SensorAmbientalSCE("AMB-01", self.sensor_amb_sim)
        self.fusionador = FusionadorDatos()
        self.controlador = ControladorNivel(H_max=200, umbral_bajo=30, umbral_alto=170)
        
        # Almacenamiento
        self.db = AlmacenamientoLocal()
        
        # Planificador
        self.scheduler = PlanificadorCiclico()
        
        # Variables de estado
        self.temp_actual = 25
        self.presion_actual = 1013
        self.nivel_fusionado = 50
        
        print("✅ Sistema inicializado")
        
    def tarea_adquisicion_fusion(self):
        """T1: Adquirir datos de sensores y fusionar"""
        # Actualizar física del tanque
        self.tanque.actualizar(dt=0.1)
        
        # Leer sensores ambientales
        self.temp_actual = self.sensor_amb.leer_T()
        self.presion_actual = self.sensor_amb.leer_P()
        
        # Leer sensor ultrasónico
        d_cruda = self.sensor_us.medir_TOF(
            self.tanque.nivel_actual, 
            self.temp_actual, 
            self.presion_actual
        )
        
        # Fusión de datos
        self.nivel_fusionado = self.fusionador.ejecutar_fusion(
            d_cruda, self.temp_actual, self.presion_actual, 200
        )
    
    def tarea_control(self):
        """T2: Lógica de control"""
        self.controlador.procesar_lectura(self.nivel_fusionado)
        accion = self.controlador.ejecutar_logica_control()
        
        # Actuar sobre válvulas simuladas
        if accion == "ACTIVAR_ENTRADA":
            self.tanque.set_valvula_entrada(True)
            self.tanque.set_bomba_salida(False)
        elif accion == "ACTIVAR_SALIDA":
            self.tanque.set_valvula_entrada(False)
            self.tanque.set_bomba_salida(True)
        else:
            self.tanque.set_valvula_entrada(True)
            self.tanque.set_bomba_salida(False)
        
        self.controlador.activar_alarma()
    
    def tarea_almacenamiento(self):
        """T3: Guardar datos en BD"""
        self.db.guardar(
            self.nivel_fusionado,
            self.temp_actual,
            self.presion_actual,
            self.controlador.Estado_Alarma
        )
    
    def tarea_comunicacion(self):
        """T4: Enviar datos por red (simulado)"""
        print(f"📡 [MQTT] Publicando datos: nivel={self.nivel_fusionado:.2f} cm")
    
    def ejecutar(self, duracion_segundos=60):
        """Ejecutar simulación"""
        print(f"\n🚀 Iniciando simulación por {duracion_segundos} segundos...")
        print("=" * 70)
        
        frames_totales = int(duracion_segundos / 0.1)
        
        for i in range(frames_totales):
            tareas = self.scheduler.ejecutar_frame(self)
            
            # Log cada segundo
            if i % 10 == 0:
                print(f"⏱️  t={i*0.1:6.1f}s | "
                      f"Nivel Real: {self.tanque.nivel_actual:6.2f} | "
                      f"Fusionado: {self.nivel_fusionado:6.2f} | "
                      f"Estado: {self.controlador.Estado_Alarma:12s} | "
                      f"Tareas: {','.join(tareas)}")
            
            time.sleep(0.01)  # 10ms real = 100ms simulado (acelerar 10x)
        
        print("=" * 70)
        self.db.cerrar()
        print("✅ Simulación completada")
        print(f"📊 Datos guardados en: datos/datos_sce.db")

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Gemelo Digital SCE')
    parser.add_argument('-t', '--tiempo', type=int, default=60, 
                        help='Duración de la simulación en segundos (default: 60)')
    args = parser.parse_args()
    
    sistema = SistemaGemeloDigital()
    sistema.ejecutar(duracion_segundos=args.tiempo)
EOF

echo -e "${GREEN}✓ sce_gemelo_digital.py creado${NC}"

# ==================== MACHINE LEARNING ====================
echo -e "${BLUE}📝 Creando ml_prediccion.py...${NC}"
cat > ml/ml_prediccion.py << 'EOF'
"""
Machine Learning - Predicción de Niveles
Random Forest Regressor para predicción temporal
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import sqlite3
import matplotlib.pyplot as plt
import joblib
import os

class PredictorNivel:
    """Predictor de niveles usando Random Forest"""
    def __init__(self, db_file="../datos/datos_sce.db"):
        self.db_file = db_file
        self.modelo = None
        self.scaler_X = None
        self.scaler_y = None
        
    def cargar_datos(self):
        """Cargar datos desde SQLite"""
        if not os.path.exists(self.db_file):
            raise FileNotFoundError(f"❌ Base de datos no encontrada: {self.db_file}")
        
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query("SELECT * FROM mediciones", conn)
        conn.close()
        
        if df.empty:
            raise ValueError("❌ No hay datos en la base de datos")
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        print(f"✅ Cargados {len(df)} registros")
        return df
    
    def crear_features(self, df, ventana=5):
        """
        Crear features para ML:
        - Niveles en t-1, t-2, ..., t-n
        - Temperatura actual
        - Presión actual
        - Diferencia de nivel (tendencia)
        """
        features = []
        targets = []
        
        for i in range(ventana, len(df)):
            feat = []
            
            # Niveles históricos
            for j in range(ventana):
                feat.append(df.iloc[i-ventana+j]['nivel'])
            
            # Características ambientales
            feat.append(df.iloc[i]['temperatura'])
            feat.append(df.iloc[i]['presion'])
            
            # Tendencia (diferencia primer orden)
            tendencia = df.iloc[i-1]['nivel'] - df.iloc[i-ventana]['nivel']
            feat.append(tendencia)
            
            features.append(feat)
            targets.append(df.iloc[i]['nivel'])
        
        return np.array(features), np.array(targets)
    
    def entrenar(self, test_size=0.2, n_estimators=100):
        """Entrenar Random Forest"""
        print("\n🧠 Entrenando modelo de Machine Learning...")
        print("=" * 50)
        
        df = self.cargar_datos()
        X, y = self.crear_features(df, ventana=5)
        
        print(f"📊 Conjunto de datos:")
        print(f"   - Features: {X.shape}")
        print(f"   - Target: {y.shape}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, shuffle=False
        )
        
        print(f"   - Train: {len(X_train)} muestras")
        print(f"   - Test: {len(X_test)} muestras")
        
        # Entrenar modelo
        print(f"\n🔧 Configuración Random Forest:")
        print(f"   - n_estimators: {n_estimators}")
        print(f"   - max_depth: 15")
        
        self.modelo = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.modelo.fit(X_train, y_train)
        
        # Evaluar
        y_pred_train = self.modelo.predict(X_train)
        y_pred_test = self.modelo.predict(X_test)
        
        mse_train = mean_squared_error(y_train, y_pred_train)
        mse_test = mean_squared_error(y_test, y_pred_test)
        mae_test = mean_absolute_error(y_test, y_pred_test)
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        
        print(f"\n📈 Resultados del entrenamiento:")
        print(f"   Train MSE: {mse_train:.4f} | R²: {r2_train:.4f}")
        print(f"   Test  MSE: {mse_test:.4f} | R²: {r2_test:.4f}")
        print(f"   Test  MAE: {mae_test:.4f} cm")
        
        # Graficar resultados
        self._graficar_resultados(y_test, y_pred_test)
        
        # Importancia de features
        self._graficar_importancia()
        
        print("=" * 50)
        return {'mse_test': mse_test, 'r2_test': r2_test, 'mae_test': mae_test}
    
    def _graficar_resultados(self, y_test, y_pred):
        """Graficar predicciones vs reales"""
        plt.figure(figsize=(14, 5))
        
        # Subplot 1: Serie temporal
        plt.subplot(1, 2, 1)
        n_puntos = min(200, len(y_test))
        plt.plot(y_test[:n_puntos], label='Real', marker='o', markersize=3, alpha=0.7)
        plt.plot(y_pred[:n_puntos], label='Predicción', marker='x', markersize=3, alpha=0.7)
        plt.legend()
        plt.title("Predicción de Nivel - Serie Temporal")
        plt.xlabel("Muestra")
        plt.ylabel("Nivel (cm)")
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Scatter plot
        plt.subplot(1, 2, 2)
        plt.scatter(y_test, y_pred, alpha=0.5, s=10)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.title("Predicción vs Real")
        plt.xlabel("Nivel Real (cm)")
        plt.ylabel("Nivel Predicho (cm)")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig("../resultados/prediccion_ml.png", dpi=300, bbox_inches='tight')
        print(f"💾 Gráfica guardada: resultados/prediccion_ml.png")
        plt.close()
    
    def _graficar_importancia(self):
        """Graficar importancia de features"""
        if self.modelo is None:
            return
        
        importancias = self.modelo.feature_importances_
        features = [f'Nivel t-{i}' for i in range(5, 0, -1)] + ['Temp', 'Presión', 'Tendencia']
        
        plt.figure(figsize=(10, 6))
        indices = np.argsort(importancias)[::-1]
        plt.bar(range(len(importancias)), importancias[indices])
        plt.xticks(range(len(importancias)), [features[i] for i in indices], rotation=45)
        plt.title("Importancia de Features - Random Forest")
        plt.ylabel("Importancia")
        plt.tight_layout()
        plt.savefig("../resultados/importancia_features.png", dpi=300, bbox_inches='tight')
        print(f"💾 Gráfica guardada: resultados/importancia_features.png")
        plt.close()
    
    def predecir_futuro(self, ultimos_datos, temp=25, presion=1013, pasos=10):
        """Predecir los próximos N pasos"""
        if self.modelo is None:
            raise ValueError("❌ Modelo no entrenado")
        
        predicciones = []
        datos = list(ultimos_datos[-5:])  # Últimos 5 niveles
        
        for _ in range(pasos):
            # Crear feature vector
            tendencia = datos[-1] - datos[0]
            X = np.array(datos[-5:] + [temp, presion, tendencia]).reshape(1, -1)
            
            # Predecir
            pred = self.modelo.predict(X)[0]
            predicciones.append(pred)
            datos.append(pred)
        
        return predicciones
    
    def guardar_modelo(self, filename="../ml/modelo_rf.pkl"):
        """Guardar modelo entrenado"""
        if self.modelo is None:
            raise ValueError("❌ No hay modelo para guardar")
        
        joblib.dump(self.modelo, filename)
        print(f"💾 Modelo guardado: {filename}")
    
    def cargar_modelo(self, filename="../ml/modelo_rf.pkl"):
        """Cargar modelo pre-entrenado"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"❌ Modelo no encontrado: {filename}")
        
        self.modelo = joblib.load(filename)
        print(f"📂 Modelo cargado: {filename}")

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    print("🤖 Sistema de Predicción de Niveles con Machine Learning")
    print("=" * 60)
    
    predictor = PredictorNivel()
    
    try:
        # Entrenar
        metricas = predictor.entrenar(n_estimators=100)
        
        # Guardar modelo
        predictor.guardar_modelo()
        
        # Ejemplo de predicción futura
        print("\n🔮 Ejemplo de predicción futura:")
        ultimos = [100, 105, 110, 112, 115]
        print(f"   Últimos 5 niveles: {ultimos}")
        futuro = predictor.predecir_futuro(ultimos, pasos=10)
        print(f"   Predicción próximos 10 pasos:")
        for i, pred in enumerate(futuro, 1):
            print(f"      t+{i}: {pred:.2f} cm")
        
        print("\n✅ Proceso completado exitosamente")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("💡 Primero debe ejecutar: python sce/sce_gemelo_digital.py")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
EOF

echo -e "${GREEN}✓ ml_prediccion.py creado${NC}"

# ==================== DASHBOARD ====================
echo -e "${BLUE}📝 Creando dashboard_streamlit.py...${NC}"
cat > dashboard/dashboard_streamlit.py << 'EOF'
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
    db_path = "../datos/datos_sce.db"
    
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
st.markdown("---")

# Sidebar
st.sidebar.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=SCE+UDO", use_container_width=True)
st.sidebar.header("⚙️ Configuración")
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (cada 2s)", value=False)
n_muestras = st.sidebar.slider("📊 Muestras a mostrar", 50, 1000, 500, 50)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📘 Información")
st.sidebar.info(
    """
    **Equipo:**
    - Ing. Torres Rousemery
    - Ing. Pinto Adrian
    - Ing. Cova Luis
    
    **Universidad de Oriente**
    Postgrado en Ingeniería Eléctrica
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
EOF

echo -e "${GREEN}✓ dashboard_streamlit.py creado${NC}"

# ==================== REQUIREMENTS ====================
echo -e "${BLUE}📝 Creando requirements.txt...${NC}"
cat > requirements.txt << 'EOF'
# Dependencias del proyecto SCE Gemelo Digital
# Python >= 3.8

# Computación científica
numpy>=1.21.0
scipy>=1.7.0

# Análisis de datos
pandas>=1.3.0

# Machine Learning
scikit-learn>=1.0.0
joblib>=1.1.0

# Visualización
matplotlib>=3.4.0
plotly>=5.0.0

# Dashboard web
streamlit>=1.25.0

# Base de datos
# sqlite3 viene incluido en Python

# Utilidades
python-dateutil>=2.8.0
EOF

echo -e "${GREEN}✓ requirements.txt creado${NC}"

# ==================== README ====================
echo -e "${BLUE}📝 Creando README.md...${NC}"
cat > README.md << 'EOF'
# 🌊 SCE Gemelo Digital - Sistema de Monitoreo de Nivel

**Evaluación 3 - Microprocesadores Aplicados a Control**

Sistema Computacional Empotrado (SCE) completamente simulado con:
- ✅ Gemelo Digital del sistema físico
- ✅ Programación Orientada a Objetos (POO)
- ✅ Planificador Ejecutivo Cíclico (Tiempo Real)
- ✅ Fusión de Datos Multisensor
- ✅ Machine Learning (Predicción con Random Forest)
- ✅ Dashboard Web Interactivo

---

## 👥 Equipo

- **Ing. Torres Rousemery**
- **Ing. Pinto Adrian**
- **Ing. Cova Luis**

**Universidad de Oriente - Núcleo Anzoátegui**  
Postgrado en Ingeniería Eléctrica  
Especialización en Automatización e Informática Industrial

---

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
