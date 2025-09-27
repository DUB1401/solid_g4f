from Source.Structs.Options import Options
from Source.Generators import Generate

from dublib.Methods.Filesystem import ReadTextFile

from typing import Optional
import logging

from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import FastAPI

api = FastAPI()

logging.basicConfig(
	filename = "logs.log",
	encoding = "utf-8",
	level = logging.INFO,
	format = "%(asctime)s %(levelname)s: %(message)s",
	datefmt = "%Y-%m-%d %H:%M:%S"
)

class RequestData(BaseModel):
	"""Структура запроса."""
	
	request: str
	length: Optional[int] = None
	language: Optional[str] = None
	model: Optional[str] = None
	tries: Optional[int] = 3
	timeout: Optional[int] = 30
	proxy: Optional[bool] = False

@api.get("/")
def generate():		
	return HTMLResponse(ReadTextFile("Docs/API.html"))

@api.post("/generate")
def generate(data: RequestData):
	CurrentOptions = Options()
	CurrentOptions.set_language(data.language)
	CurrentOptions.set_max_length(data.length)
	CurrentOptions.set_tries(data.tries)
	CurrentOptions.set_timeout(data.timeout)
	CurrentOptions.set_model(data.model)
	CurrentOptions.set_force_proxy(data.proxy)
	Response = Generate(data.request, CurrentOptions)
									
	return Response.to_dict()