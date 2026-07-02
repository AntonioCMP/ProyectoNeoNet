# 🚀 NeoNet - Clasificador Inteligente de Perfiles de Inversión

> **Plataforma educativa de análisis y recomendación de portafolios de inversión basada en Inteligencia Artificial**

![Status](https://img.shields.io/badge/status-Active-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![License](https://img.shields.io/badge/License-Educational%20Use-yellow?style=flat-square)

---

## 📋 Tabla de Contenidos
- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Características Principales](#-características-principales)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso de la Aplicación](#-uso-de-la-aplicación)
- [Equipo de Desarrollo](#-equipo-de-desarrollo)
- [Licencia](#-licencia)

---

## 💡 Descripción del Proyecto

**NeoNet** es una aplicación web interactiva desarrollada como proyecto educativo universitario que utiliza **Machine Learning** y **análisis técnico de datos** para clasificar perfiles de inversión y proporcionar recomendaciones de portafolios personalizados.

A través de un cuestionario inteligente, la aplicación determina el perfil de riesgo del usuario (Conservador, Moderado o Arriesgado) y genera recomendaciones de activos que se alinean con su estrategia de inversión.

### Objetivo Educativo
Este proyecto integra conceptos de:
- 🤖 Machine Learning (Random Forest Classification)
- 📊 Análisis Técnico de Mercados Financieros
- 💻 Desarrollo Full-Stack Web
- 📈 Data Science y Feature Engineering
- 🔄 APIs REST con FastAPI

---

## ✨ Características Principales

### 🎯 Clasificación de Perfiles de Inversor
- **Análisis basado en cuestionario** con parámetros financieros y demográficos
- **Modelo ML entrenado** con Random Forest usando dataset de comportamiento financiero
- **3 perfiles identificados**: Conservador, Moderado y Arriesgado

### 📊 Portafolios Recomendados
Cada perfil incluye una cartera de activos curada:
- **Conservador**: Acciones de dividendo, bonos, ETFs defensivos y oro
- **Moderado**: Mezcla equilibrada de tech, financiero y bienes de consumo
- **Arriesgado**: Empresas tecnológicas, criptomonedas y startups innovadoras

### 🤖 Bot de Análisis Técnico
- Análisis de tendencias mediante **medias móviles** (corta y larga)
- Integración con **Yahoo Finance API** para datos reales
- Decisiones automáticas: COMPRAR, VENDER, MANTENER
- Cálculo de volatilidad y registro de operaciones

### 🎨 Interfaz Moderna
- Diseño responsivo con Bootstrap 5
- Paleta de colores corporativa profesional
- UX optimizada con transiciones suaves
- Emojis contextuales para mejor comprensión

---

## 🛠️ Tecnologías Utilizadas

### Backend
```
FastAPI          - Framework web asincrónico de alto rendimiento
Python 3.8+      - Lenguaje principal
scikit-learn     - Modelos de ML (Random Forest)
XGBoost          - Alternativa de modelos de boosting
yfinance         - API para datos de Yahoo Finance
pandas           - Análisis y manipulación de datos
numpy            - Cálculos numéricos
```

### Frontend
```
HTML5 + Bootstrap 5  - Estructura y estilos responsivos
Jinja2 Templates     - Renderizado dinámico de plantillas
JavaScript Vanilla   - Interactividad del cliente
CSS Custom Props     - Temas y personalización
```

### Datos y Entrenamiento
```
Jupyter Notebook    - Exploración y análisis de datos
scikit-learn        - Preprocesamiento y evaluación de modelos
Pandas              - Limpieza y transformación de datos
```

---

## 🏗️ Arquitectura del Sistema

```
NeoNet/
│
├── 📁 aplicacion/                    # Aplicación principal
│   ├── main.py                       # Punto de entrada (servidor FastAPI)
│   │
│   ├── 📁 backend/
│   │   ├── 📁 logicaml/             # Lógica de Machine Learning
│   │   │   └── predarbol.py         # Modelo clasificador de perfiles
│   │   │
│   │   └── 📁 logicabot/            # Bot de análisis técnico
│   │       └── bot.py               # Análisis de tendencias y medias móviles
│   │
│   ├── 📁 frontend/                  # Interfaces web
│   │   ├── cuestionario.html         # Formulario de evaluación
│   │   └── bot.html                  # Panel de análisis técnico
│   │
│   └── 📁 static/                    # Recursos estáticos
│       └── logo_nn.jpeg              # Identidad visual
│
└── 📁 EntrenamientoBosque/           # Notebooks de entrenamiento
    ├── script_ebosque.ipynb          # Pipeline de ML
    └── 📁 data/
        └── Finance_Trends.csv        # Dataset de entrenamiento
```

### Flujo de Datos

```
Usuario
   ↓
[Cuestionario HTML] → [FastAPI Backend]
   ↓                         ↓
[Respuestas]        [Modelo ML (predarbol.py)]
   ↓                         ↓
                    [Clasificación de Perfil]
   ↓                         ↓
[Portafolio Recomendado] ← [Bot de Análisis] → [Yahoo Finance]
   ↓
[Respuesta JSON con activos, análisis técnico]
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (administrador de paquetes)
- Virtual Environment (recomendado)

### Paso 1: Clonar el Repositorio
```bash
cd tu/ruta/del/proyecto
```

### Paso 2: Crear Entorno Virtual
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install fastapi uvicorn python-dotenv pandas numpy scikit-learn xgboost yfinance jinja2
```

### Paso 4: Configurar Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
LOGO_URL=/static/logo_nn.jpeg
FRONTEND_PATH=aplicacion/frontend
STATIC_PATH=aplicacion/static
MODEL_PATH=ruta/al/modelo/entrenado.pickle
```

### Paso 5: Ubicar Modelo Entrenado
El archivo `predarbol.pickle` debe estar en la ruta especificada en `MODEL_PATH`

### Paso 6: Ejecutar la Aplicación
```bash
cd aplicacion
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La aplicación estará disponible en: **http://localhost:8000**

---

## 📖 Uso de la Aplicación

### 1️⃣ Completar Cuestionario de Inversión

Accede a la interfaz inicial donde deberás responder preguntas sobre:
- **Información demográfica** (edad, género)
- **Experiencia inversora** (expectativas de retorno, riesgo)
- **Horizonte temporal** (duración de la inversión)
- **Objetivos financieros** (ahorro, creación de riqueza)

### 2️⃣ Recibir Clasificación

El sistema procesará tus respuestas mediante el **modelo Random Forest** entrenado y te asignará un perfil:
- 🛡️ **Conservador**: Para inversores cautelosos
- ⚖️ **Moderado**: Para inversores equilibrados  
- 🚀 **Arriesgado**: Para inversores agresivos

### 3️⃣ Explorar Portafolio Recomendado

Visualiza los 19 activos recomendados específicos para tu perfil, incluyendo:
- Nombre y ticker de la empresa
- Emoji representativo
- Sector y características del activo

### 4️⃣ Análisis Técnico (Bot)

Utiliza el bot para analizar cualquier ticker:
- Histórico de precios (últimos 3 meses)
- Medias móviles (5 y 20 días)
- Volatilidad anualizada
- Recomendación: COMPRAR / VENDER / MANTENER

---

## 📚 Componentes Técnicos Detallados

### ModeloInversor (predarbol.py)
```python
# Carga un modelo pre-entrenado (Random Forest)
# Entrada: diccionario con características del usuario
# Salida: clasificación en uno de los 3 perfiles
```

**Características esperadas:**
- age, gender, expectativas de retorno, duración, objetivos, etc.
- Procesadas mediante one-hot encoding
- Inferencia en tiempo real

### BotInversiones (bot.py)
```python
# Análisis técnico con medias móviles
# Ventana corta: últimos 5 días
# Ventana larga: últimos 20 días
# Decisión basada en cruce de medias
```

**Métricas calculadas:**
- Media móvil simple (SMA)
- Volatilidad histórica anualizada
- Tendencia (ALCISTA / BAJISTA / NEUTRAL)

---

## 📊 Dataset de Entrenamiento

**Archivo:** `Finance_Trends.csv` en `EntrenamientoBosque/data/`

- **Origen**: Comportamiento financiero y tendencias de mercado
- **Muestras**: Cientos de registros de inversores categorizados
- **Features**: Preferencias por tipo de activo (acciones, bonos, fondos mutuos, criptomonedas, etc.)
- **Target**: Clasificación en 3 perfiles de riesgo

**Procesamiento:**
- Eliminación de valores nulos
- Removimiento de duplicados
- Feature engineering: Score_Riesgo, Score_Seguro
- Train-test split para validación

---

## 👥 Equipo de Desarrollo

| Nombre | Rol |
|--------|-----|
| **Antonio Calderón** | Desarrollo Full-Stack |
| **Oriana Ochoa** | Análisis de Datos & ML |
| **Gabriela Padilla** | Interfaz & UX |
| **Juan Diego Ruales** | Análisis Técnico & Bot |

**Universidad:** [Tu Universidad]  
**Semestre:** 4to Semestre  
**Fecha de Desarrollo:** 2024

---

## 📝 Licencia

Este proyecto es de **uso educativo exclusivamente** bajo fines académicos.

---

## 🔗 Recursos Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn ML](https://scikit-learn.org/)
- [Yahoo Finance API](https://finance.yahoo.com/)
- [Bootstrap 5](https://getbootstrap.com/)

---

## 📞 Notas Importantes

⚠️ **Descargo de Responsabilidad Financiera**  
NeoNet es una herramienta educativa. Las recomendaciones generadas NO son asesoramiento financiero profesional. Antes de realizar inversiones reales, consulta con un asesor financiero certificado.

---

**Hecho con ❤️ para la educación en Finanzas e Inteligencia Artificial**