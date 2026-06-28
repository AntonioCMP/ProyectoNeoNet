
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from backend.logicaml.predarbol import ModeloInversor
from backend.logicabot.bot import BotInversiones

app = FastAPI()
templates = Jinja2Templates(directory="D:\\DocumentosI\\EDUCATIVA+\\4to Semestre\\ProyectoNeoNet\\aplicacion\\frontend")

clasificador_arbol = ModeloInversor()
# Usamos medias de 5 y 20 días que son estándar en trading de corto plazo
bot_predictivo = BotInversiones(ventana_corta=5, ventana_larga=20)


PORTAFOLIOS = {
    "Conservador": [
        {"ticker": "JNJ", "nombre": "Johnson & Johnson (Farmacéutica)"},
        {"ticker": "KO", "nombre": "Coca-Cola (Consumo Defensivo)"},
        {"ticker": "PG", "nombre": "Procter & Gamble (Consumo Defensivo)"},
        {"ticker": "PEP", "nombre": "PepsiCo (Consumo Defensivo)"},
        {"ticker": "WMT", "nombre": "Walmart (Retail Defensivo)"},
        {"ticker": "MCD", "nombre": "McDonald's (Restaurantes)"},
        {"ticker": "CL", "nombre": "Colgate-Palmolive (Consumo Básico)"},
        {"ticker": "K", "nombre": "Kellanova / Kellogg's (Alimentos)"},
        {"ticker": "GIS", "nombre": "General Mills (Alimentos)"},
        {"ticker": "VZ", "nombre": "Verizon (Telecomunicaciones)"},
        {"ticker": "T", "nombre": "AT&T (Telecomunicaciones)"},
        {"ticker": "DUK", "nombre": "Duke Energy (Servicios Públicos)"},
        {"ticker": "SO", "nombre": "Southern Company (Servicios Eléctricos)"},
        {"ticker": "NEE", "nombre": "NextEra Energy (Energías Renovables)"},
        {"ticker": "LMT", "nombre": "Lockheed Martin (Defensa)"},
        {"ticker": "PFE", "nombre": "Pfizer (Farmacéutica)"},
        {"ticker": "MRK", "nombre": "Merck & Co. (Farmacéutica)"},
        {"ticker": "TLT", "nombre": "ETF Bonos del Tesoro EE.UU. 20+ años"},
        {"ticker": "AGG", "nombre": "ETF Bonos Agregados EE.UU."},
        {"ticker": "GLD", "nombre": "ETF Oro Físico (Refugio Seguro)"}
    ],
    "Moderado": [
        {"ticker": "SPY", "nombre": "S&P 500 ETF (Mercado General)"},
        {"ticker": "QQQ", "nombre": "Nasdaq 100 ETF (Tecnología)"},
        {"ticker": "AAPL", "nombre": "Apple Inc. (Hardware/Servicios)"},
        {"ticker": "MSFT", "nombre": "Microsoft Corp. (Software/Nube)"},
        {"ticker": "GOOGL", "nombre": "Alphabet / Google (Publicidad/Nube)"},
        {"ticker": "AMZN", "nombre": "Amazon (E-commerce/Nube)"},
        {"ticker": "META", "nombre": "Meta Platforms (Redes Sociales)"},
        {"ticker": "BRK-B", "nombre": "Berkshire Hathaway (Holding)"},
        {"ticker": "V", "nombre": "Visa Inc. (Pagos Globales)"},
        {"ticker": "MA", "nombre": "Mastercard (Pagos Globales)"},
        {"ticker": "JPM", "nombre": "JPMorgan Chase (Banca)"},
        {"ticker": "BAC", "nombre": "Bank of America (Banca)"},
        {"ticker": "HD", "nombre": "Home Depot (Mejoras para el hogar)"},
        {"ticker": "COST", "nombre": "Costco Wholesale (Retail)"},
        {"ticker": "DIS", "nombre": "Walt Disney Co. (Entretenimiento)"},
        {"ticker": "NKE", "nombre": "Nike Inc. (Ropa Deportiva)"},
        {"ticker": "SBUX", "nombre": "Starbucks (Bebidas/Retail)"},
        {"ticker": "UNH", "nombre": "UnitedHealth Group (Seguros Médicos)"},
        {"ticker": "ABBV", "nombre": "AbbVie (Biotecnología/Farmacéutica)"},
        {"ticker": "CRM", "nombre": "Salesforce (Software en la Nube)"}
    ],
    "Arriesgado": [
        {"ticker": "TSLA", "nombre": "Tesla Inc. (Vehículos Eléctricos)"},
        {"ticker": "NVDA", "nombre": "Nvidia Corp. (Semiconductores/IA)"},
        {"ticker": "AMD", "nombre": "Advanced Micro Devices (Semiconductores)"},
        {"ticker": "COIN", "nombre": "Coinbase (Exchange de Criptomonedas)"},
        {"ticker": "MSTR", "nombre": "MicroStrategy (Proxy de Bitcoin)"},
        {"ticker": "MARA", "nombre": "Marathon Digital (Minería Cripto)"},
        {"ticker": "RIOT", "nombre": "Riot Platforms (Minería Cripto)"},
        {"ticker": "PLTR", "nombre": "Palantir Technologies (Software/IA)"},
        {"ticker": "SNOW", "nombre": "Snowflake (Datos en la Nube)"},
        {"ticker": "CRWD", "nombre": "CrowdStrike (Ciberseguridad)"},
        {"ticker": "SQ", "nombre": "Block / Square (Fintech)"},
        {"ticker": "ROKU", "nombre": "Roku Inc. (Streaming)"},
        {"ticker": "UBER", "nombre": "Uber Technologies (Movilidad)"},
        {"ticker": "ABNB", "nombre": "Airbnb (Turismo/Alojamiento)"},
        {"ticker": "DASH", "nombre": "DoorDash (Delivery)"},
        {"ticker": "SHOP", "nombre": "Shopify (E-commerce B2B)"},
        {"ticker": "HOOD", "nombre": "Robinhood (Broker Fintech)"},
        {"ticker": "SMCI", "nombre": "Super Micro Computer (Hardware IA)"},
        {"ticker": "NIO", "nombre": "NIO Inc. (Vehículos Eléctricos China)"},
        {"ticker": "ARKK", "nombre": "ARK Innovation ETF (Innovación Disruptiva)"}
    ]
}

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(name="cuestionario.html", request= request)

@app.post("/predecir_perfil", response_class=HTMLResponse)
async def procesar_cuestionario(
    request: Request,
    age: int = Form(...), gender: str = Form(...), factor: str = Form(...),
    objective: str = Form(...), purpose: str = Form(...), 
    duration: str = Form(...), expect: str = Form(...)
):
    datos = {
        "age": age, "gender": gender, "Factor": factor, "Objective": objective,
        "Purpose": purpose, "Duration": duration, "Expect": expect
    }
    
    perfil = clasificador_arbol.predecir_perfil(datos)
    activos_recomendados = PORTAFOLIOS.get(perfil, [])
    
    return templates.TemplateResponse(name="cuestionario.html", context={
        "request": request, 
        "resultado": perfil,
        "activos": activos_recomendados
    })

@app.get("/bot", response_class=HTMLResponse)
async def dashboard_bot(request: Request, ticker: str = "AAPL"):
  
    return templates.TemplateResponse(name="bot.html", context={
        "request": request, 
        "ticker_inicial": ticker
    })

@app.get("/api/bot/analizar/{ticker}")
async def analizar_ticker(ticker: str):
    
    resultado = bot_predictivo.analizar_accion_yahoo(ticker)
   
    auditoria = bot_predictivo.auditar_historial()
    
    return JSONResponse(content={
        "analisis": resultado,
        "auditoria": auditoria
    })

if __name__ == "__main__":
 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)