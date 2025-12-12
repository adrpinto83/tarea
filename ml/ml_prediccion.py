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
    def __init__(self, db_file=None):
        if db_file is None:
            # Usar ruta absoluta basada en el directorio raíz del proyecto
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            db_file = os.path.join(base_dir, "datos", "datos_sce.db")
        self.db_file = db_file
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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
        output_path = os.path.join(self.base_dir, "resultados", "prediccion_ml.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"💾 Gráfica guardada: {output_path}")
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
        output_path = os.path.join(self.base_dir, "resultados", "importancia_features.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"💾 Gráfica guardada: {output_path}")
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
    
    def guardar_modelo(self, filename=None):
        """Guardar modelo entrenado"""
        if self.modelo is None:
            raise ValueError("❌ No hay modelo para guardar")

        if filename is None:
            filename = os.path.join(self.base_dir, "ml", "modelo_rf.pkl")

        joblib.dump(self.modelo, filename)
        print(f"💾 Modelo guardado: {filename}")

    def cargar_modelo(self, filename=None):
        """Cargar modelo pre-entrenado"""
        if filename is None:
            filename = os.path.join(self.base_dir, "ml", "modelo_rf.pkl")

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
