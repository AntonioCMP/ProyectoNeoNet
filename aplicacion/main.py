
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles # <-- Nueva importación para servir la imagen
import uvicorn

from backend.logicaml.predarbol import ModeloInversor
from backend.logicabot.bot import BotInversiones

# Cargar variables de entorno
load_dotenv()
LOGO_URL = os.getenv("LOGO_URL", "https://via.placeholder.com/150")

app = FastAPI()

# Montar la carpeta estática para que FastAPI pueda mostrar el logo
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="D:\\DocumentosI\\EDUCATIVA+\\4to Semestre\\ProyectoNeoNet\\aplicacion\\frontend")

clasificador_arbol = ModeloInversor()
bot_predictivo = BotInversiones(ventana_corta=5, ventana_larga=20)

# ... [MANTÉN TU DICCIONARIO PORTAFOLIOS AQUÍ CON LOS EMOJIS] ...

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="cuestionario.html", 
        context={"logo_url": LOGO_URL} # <-- Pasamos el logo
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
            "logo_url": LOGO_URL # <-- Pasamos el logo
        }
    )

@app.get("/bot", response_class=HTMLResponse)
async def dashboard_bot(request: Request, ticker: str = "AAPL"):
    return templates.TemplateResponse(
        request=request,
        name="bot.html", 
        context={
            "ticker_inicial": ticker,
            "logo_url": LOGO_URL # <-- Pasamos el logo
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