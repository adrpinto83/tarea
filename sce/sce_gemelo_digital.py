"""
Sistema Computacional Empotrado - Gemelo Digital
Implementación con POO y Planificador Ejecutivo Cíclico
"""
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    def __init__(self, db_file=None):
        if db_file is None:
            # Usar ruta absoluta basada en el directorio raíz del proyecto
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            db_file = os.path.join(base_dir, "datos", "datos_sce.db")
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
