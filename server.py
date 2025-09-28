from Source.Structs.Options import Options
from Source.Generators import Generate
from Source.Initializator import *

from dublib.Methods.Filesystem import ReadTextFile

from typing import Optional, Literal

from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import FastAPI

api = FastAPI()

class RequestData(BaseModel):
	"""Структура запроса."""
	
	request: str
	length: Optional[int] = None
	language: Optional[str] = None
	model: Optional[str] = None
	tries: Optional[int] = 3
	timeout: Optional[int] = 30
	proxy: Optional[bool] = False
	source: Literal["gpt4free", "gemini"] = "gpt4free"

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
	CurrentOptions.select_source(data.source)

	Response = Generate(data.request, CurrentOptions)
									
	return Response.to_dict()