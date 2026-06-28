
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
import uvicorn

from backend.logicaml.predarbol import ModeloInversor
from backend.logicabot.bot import BotInversiones

load_dotenv()
LOGO_URL = os.getenv("LOGO_URL", "/static/logo_nn.jpeg")
FRONTEND_PATH = os.getenv("FRONTEND_PATH", "frontend")
STATIC_PATH = os.getenv("STATIC_PATH", "static")

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

templates = Jinja2Templates(directory=FRONTEND_PATH)

clasificador_arbol = ModeloInversor()
bot_predictivo = BotInversiones(ventana_corta=5, ventana_larga=20)

PORTAFOLIOS = {
    "Conservador": [
        {"ticker": "JNJ", "nombre": "Johnson & Johnson", "emoji": "💊"},
        {"ticker": "KO", "nombre": "Coca-Cola", "emoji": "🥤"},
        {"ticker": "PG", "nombre": "Procter & Gamble", "emoji": "🧼"},
        {"ticker": "PEP", "nombre": "PepsiCo", "emoji": "🥤"},
        {"ticker": "WMT", "nombre": "Walmart", "emoji": "🛒"},
        {"ticker": "MCD", "nombre": "McDonald's", "emoji": "🍔"},
        {"ticker": "CL", "nombre": "Colgate-Palmolive", "emoji": "🪥"},
        {"ticker": "K", "nombre": "Kellanova", "emoji": "🥣"},
        {"ticker": "GIS", "nombre": "General Mills", "emoji": "🌾"},
        {"ticker": "VZ", "nombre": "Verizon", "emoji": "📱"},
        {"ticker": "T", "nombre": "AT&T", "emoji": "📞"},
        {"ticker": "DUK", "nombre": "Duke Energy", "emoji": "⚡"},
        {"ticker": "SO", "nombre": "Southern Company", "emoji": "🔌"},
        {"ticker": "NEE", "nombre": "NextEra Energy", "emoji": "☀️"},
        {"ticker": "LMT", "nombre": "Lockheed Martin", "emoji": "🚀"},
        {"ticker": "PFE", "nombre": "Pfizer", "emoji": "💉"},
        {"ticker": "MRK", "nombre": "Merck & Co.", "emoji": "🔬"},
        {"ticker": "TLT", "nombre": "ETF Bonos 20+ años", "emoji": "📜"},
        {"ticker": "AGG", "nombre": "ETF Bonos Agregados", "emoji": "📉"},
        {"ticker": "GLD", "nombre": "ETF Oro Físico", "emoji": "🥇"}
    ],
    "Moderado": [
        {"ticker": "SPY", "nombre": "S&P 500 ETF", "emoji": "📊"},
        {"ticker": "QQQ", "nombre": "Nasdaq 100 ETF", "emoji": "💻"},
        {"ticker": "AAPL", "nombre": "Apple Inc.", "emoji": "🍏"},
        {"ticker": "MSFT", "nombre": "Microsoft Corp.", "emoji": "🪟"},
        {"ticker": "GOOGL", "nombre": "Alphabet / Google", "emoji": "🔍"},
        {"ticker": "AMZN", "nombre": "Amazon", "emoji": "📦"},
        {"ticker": "META", "nombre": "Meta Platforms", "emoji": "🌐"},
        {"ticker": "BRK-B", "nombre": "Berkshire Hathaway", "emoji": "🏛️"},
        {"ticker": "V", "nombre": "Visa Inc.", "emoji": "💳"},
        {"ticker": "MA", "nombre": "Mastercard", "emoji": "💳"},
        {"ticker": "JPM", "nombre": "JPMorgan Chase", "emoji": "🏦"},
        {"ticker": "BAC", "nombre": "Bank of America", "emoji": "🏦"},
        {"ticker": "HD", "nombre": "Home Depot", "emoji": "🛠️"},
        {"ticker": "COST", "nombre": "Costco Wholesale", "emoji": "🛒"},
        {"ticker": "DIS", "nombre": "Walt Disney Co.", "emoji": "🎢"},
        {"ticker": "NKE", "nombre": "Nike Inc.", "emoji": "👟"},
        {"ticker": "SBUX", "nombre": "Starbucks", "emoji": "☕"},
        {"ticker": "UNH", "nombre": "UnitedHealth Group", "emoji": "🏥"},
        {"ticker": "ABBV", "nombre": "AbbVie", "emoji": "💊"},
        {"ticker": "CRM", "nombre": "Salesforce", "emoji": "☁️"}
    ],
    "Arriesgado": [
        {"ticker": "TSLA", "nombre": "Tesla Inc.", "emoji": "🚗"},
        {"ticker": "NVDA", "nombre": "Nvidia Corp.", "emoji": "🖥️"},
        {"ticker": "AMD", "nombre": "Advanced Micro Devices", "emoji": "⚙️"},
        {"ticker": "COIN", "nombre": "Coinbase", "emoji": "🪙"},
        {"ticker": "MSTR", "nombre": "MicroStrategy", "emoji": "₿"},
        {"ticker": "MARA", "nombre": "Marathon Digital", "emoji": "⛏️"},
        {"ticker": "RIOT", "nombre": "Riot Platforms", "emoji": "⛏️"},
        {"ticker": "PLTR", "nombre": "Palantir Technologies", "emoji": "👁️"},
        {"ticker": "SNOW", "nombre": "Snowflake", "emoji": "❄️"},
        {"ticker": "CRWD", "nombre": "CrowdStrike", "emoji": "🛡️"},
        {"ticker": "SQ", "nombre": "Block / Square", "emoji": "⬛"},
        {"ticker": "ROKU", "nombre": "Roku Inc.", "emoji": "📺"},
        {"ticker": "UBER", "nombre": "Uber", "emoji": "🚕"},
        {"ticker": "ABNB", "nombre": "Airbnb", "emoji": "🏠"},
        {"ticker": "DASH", "nombre": "DoorDash", "emoji": "🥡"},
        {"ticker": "SHOP", "nombre": "Shopify", "emoji": "🛍️"},
        {"ticker": "HOOD", "nombre": "Robinhood", "emoji": "🏹"},
        {"ticker": "SMCI", "nombre": "Super Micro Computer", "emoji": "🗄️"},
        {"ticker": "NIO", "nombre": "NIO Inc.", "emoji": "🔋"},
        {"ticker": "ARKK", "nombre": "ARK Innovation ETF", "emoji": "🚀"}
    ]
}

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="cuestionario.html", 
        context={"logo_url": LOGO_URL} 
    )

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
    
    return templates.TemplateResponse(
        request=request,
        name="cuestionario.html", 
        context={
            "resultado": perfil,
            "activos": activos_recomendados,
            "logo_url": LOGO_URL 
        }
    )

@app.get("/bot", response_class=HTMLResponse)
async def dashboard_bot(request: Request, ticker: str = "AAPL"):
    return templates.TemplateResponse(
        request=request,
        name="bot.html", 
        context={
            "ticker_inicial": ticker,
            "logo_url": LOGO_URL 
        }
    )

@app.get("/api/bot/analizar/{ticker}")
async def analizar_ticker(ticker: str):
    bot_predictivo = BotInversiones(ventana_corta=5, ventana_larga=20)
    
    resultado = bot_predictivo.analizar_accion_yahoo(ticker)
    auditoria = bot_predictivo.auditar_historial()
    
    return JSONResponse(content={
        "analisis": resultado,
        "auditoria": auditoria
    })

if __name__ == "__main__":
 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)