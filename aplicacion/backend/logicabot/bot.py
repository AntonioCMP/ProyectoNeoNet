
from collections import deque
import yfinance as yf
import numpy as np
import pandas as pd

class BotInversiones:
    def __init__(self, ventana_corta=5, ventana_larga=20):
        # Aumentamos las ventanas para datos
        self.ventana_larga_size = ventana_larga
        self.cola_corta = deque(maxlen=ventana_corta)
        self.cola_larga = deque(maxlen=ventana_larga)
        
        self.historial_operaciones = []
        self.estado_tendencia = "NEUTRAL"

    def procesar_precio(self, precio: float, fecha: str = "Actual"):
        self.cola_corta.append(precio)
        self.cola_larga.append(precio)

        if len(self.cola_larga) < self.ventana_larga_size:
            return {"decision": "ESPERANDO", "motivo": "Recolectando datos..."}

        media_corta = sum(self.cola_corta) / len(self.cola_corta)
        media_larga = sum(self.cola_larga) / len(self.cola_larga)

        decision = "MANTENER"
        
        if media_corta > media_larga and self.estado_tendencia != "ALCISTA":
            decision = "COMPRAR"
            self.estado_tendencia = "ALCISTA"
            self._registrar_operacion("COMPRA", precio, media_corta, media_larga, fecha)
            
        elif media_corta < media_larga and self.estado_tendencia != "BAJISTA":
            decision = "VENDER"
            self.estado_tendencia = "BAJISTA"
            self._registrar_operacion("VENTA", precio, media_corta, media_larga, fecha)

        return {
            "decision": decision, 
            "media_corta": round(media_corta, 2), 
            "media_larga": round(media_larga, 2)
        }

    def _registrar_operacion(self, tipo, precio, m_corta, m_larga, fecha):
        self.historial_operaciones.append({
            "fecha": fecha,
            "tipo": tipo,
            "precio": round(precio, 2),
            "media_corta": round(m_corta, 2),
            "media_larga": round(m_larga, 2)
        })

    def analizar_accion_yahoo(self, ticker: str, periodo="3mo"):
        """Descarga datos de Yahoo Finance, calcula volatilidad y ejecuta el algoritmo."""
    
        datos = yf.download(ticker, period=periodo, progress=False)
        if datos.empty:
            return {"error": "No se encontraron datos para el ticker"}

      
        self.cola_corta.clear()
        self.cola_larga.clear()
        self.historial_operaciones.clear()
        self.estado_tendencia = "NEUTRAL"

        
        retornos_diarios = datos['Close'].pct_change().dropna()
        volatilidad = np.std(retornos_diarios) * np.sqrt(252)

        resultado_actual = {}
      
        for fecha, fila in datos.iterrows():
            precio_cierre = float(fila['Close'].iloc[0] if isinstance(fila['Close'], pd.Series) else fila['Close'])
            fecha_str = fecha.strftime('%Y-%m-%d')
            resultado_actual = self.procesar_precio(precio_cierre, fecha_str)

        return {
            "ticker": ticker.upper(),
            "precio_actual": round(float(datos['Close'].iloc[-1]), 2),
            "volatilidad_porcentaje": round(float(volatilidad) * 100, 2),
            "decision_actual": resultado_actual.get("decision", "ESPERANDO"),
            "media_corta": resultado_actual.get("media_corta", 0),
            "media_larga": resultado_actual.get("media_larga", 0)
        }

    def auditar_historial(self):
        return self.historial_operaciones