from modules import config, database, bot

import asyncio
import httpx
import os
from fastapi import FastAPI, Depends, HTTPException, Query, Path, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from typing import Optional

#Инициализация дб и конфига
def init():
	pass

@asynccontextmanager
async def lifespan(app: FastAPI):
	yield
	print("stopped")

app = FastAPI(
	title       = "ArtemSHI API",
	summary     = "Api написано на FASTAPI",
	description = "API для работы с курсами валют и секретными ключами",
	version     = "1.0.0",
	docs_url    = "/docs", 
	openapi_url = "/openapi.json",
	lifespan=lifespan
)
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)


@app.get("/", tags = ["General"], summary = 'Главная страница')
async def public_index():
	await bot.send_message_in_channel("8239610881:AAGFNpMb29Jy2nfmeSSqO9OWkPVjRBvEVzM", -1003882117368)
	return {"message": "Successfully send message in channel"}

#КАНАЛЫ:

@app.get("/send_message_in_channel_{TOKEN}_{CHANNEL_ID}", tags = ["Channel"]) # TOKEN:str CHANNEL_ID:int ALL_DATA:dict
async def send_message_in_channel(TOKEN:str, CHANNEL_ID:int):
	print(f'DEBUG: {TOKEN}, {CHANNEL_ID}')
	try:
		await bot.send_message_in_channel(TOKEN, CHANNEL_ID, text = "test_message")
		return {"message": "Successfully send message in channel"}
	except Exception as e:
		raise JSONResponse(status_code=401, content={"ERROR": f"{e}"})

# @app.get("/send_messages_in_channels_{TOKEN}_{CHANNEL_ID}_{ALL_DATA}", tags = ["Channel"]) # TOKEN:str CHANNEL_ID:dict ALL_DATA:dict
# async def send_messages_in_channels(TOKEN:str,CHANNEL_ID:dict, ALL_DATA:dict):
# 	try:
# 		for i in CHANNEL_ID:
# 			await bot.send_message_in_channel(TOKEN, i)

# 		return {"message": "Successfully send message in channel"}
# 	except Exception as e:
# 		raise JSONResponse(status_code=401, content={"ERROR": f"{e}"})
