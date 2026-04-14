from others import config, database, bot

from fastapi import FastAPI, Depends, HTTPException, Query, Path, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.templating import Jinja2Templates

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

@app.get("/add_bot", response_class=HTMLResponse)
async def get_add_bot(request: Request):
    return templates.TemplateResponse("add_bot.html", {"request": request})

@app.get("/send_message", response_class=HTMLResponse)
async def get_send_message(request: Request):
    return templates.TemplateResponse("send_message_form.html", {"request": request})

@app.post("/send_text", tags=["Channel"], summary='Главная страница', response_model=RenderResponse)
async def send_text(request: Request):
    try:
        payload = await request.json()
        api_id = payload.get("api_id")
        api_hash = payload.get("api_hash")
        token = payload.get("token")
        chat_id = payload.get("chat_id")
        message = payload.get("message")

        missing = []
        if not api_id: missing.append("api_id")
        if not api_hash: missing.append("api_hash")
        if not token: missing.append("token")
        if not chat_id: missing.append("chat_id")
        if not message: missing.append("message")

        if missing:
            return RenderResponse(
                status="error",
                error=f"Не заполнены поля: {', '.join(missing)}"
            )

        await bot.send_message_in_channel(
            api_id=int(api_id),
            api_hash=api_hash,
            bot_token=token,
            chat_id_channel=chat_id,
            message=message
        )

        return RenderResponse(status="ok")
    except ValueError as e:
        return RenderResponse(status="error", error=f"Неверный формат api_id: {str(e)}")
    except Exception as e:
        return RenderResponse(status="error", error=f"Internal Server Error: {str(e)}")
    
@app.get("/add_bot", response_model = RenderResponse)
async def add_bot(request: Request, token: str = Form(...)):
    try:
        print(request)
        return RenderResponse(status="ok")
    except Exception as e:
        return RenderResponse(status="error", error=f"Internal Server Error: {str(e)}")
    
@app.get('/init_db', response_model=RenderResponse)
async def init_db(request: Request):
    try:
        await database.create_db()
        return RenderResponse(status="ok")
    except Exception as e:
        return RenderResponse(status="error", error=f"Internal Server Error: {str(e)}")

@app.post('/add_bot_post', response_model=RenderResponse)
async def add_bot_post(
    token: str = Form(...),
    api_id: str = Form(...),
    api_hash: str = Form(...),
):
    try:
        await database.add_bot(token=token, api_id=int(api_id), api_hash=api_hash)
        return RenderResponse(status="ok")
    except ValueError as e:
        return RenderResponse(status="error", error=f"Неверный формат api_id: {str(e)}")
    except Exception as e:
        return RenderResponse(status="error", error=f"Internal Server Error: {str(e)}")
