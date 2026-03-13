from others import config, database, bot

import asyncio
import httpx
import os
import jinja2
from fastapi import FastAPI, Depends, HTTPException, Query, Path, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.templating import Jinja2Templates
from typing import Optional

#Инициализация дб и конфига
def init():
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("stopped")

app = FastAPI(
    title       = "TeleOctopus API",
    description = "API для работы с сеткой телеграмма",
    version     = "0.1",
    docs_url    = "/docs", 
    openapi_url = "/openapi.json",
    lifespan=lifespan 
)
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class RenderResponse(BaseModel):
    status: str
    error: str | dict | None = None
    
@app.get("/",response_class = HTMLResponse)
async def public_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "Пользователь"})

@app.post("/send_text", tags = ["Channel"], summary = 'Главная страница', response_model = RenderResponse)
async def send_text(request: Request):
    try:
        request = await request.json()
        await bot.send_message_in_channel(token = request.get("token"), chat_id_channel = request.get("chat_id"), message = request.get("message"))
        
        return RenderResponse(status="ok")
    except Exception as e:
        return RenderResponse(status="error", error=f"Internal Server Error: {str(e)}")
    