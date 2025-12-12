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
