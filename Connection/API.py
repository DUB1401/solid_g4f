from .Data import Options

from dublib.WebRequestor import WebResponse

from datetime import datetime
from threading import Thread
from time import sleep
from typing import Any

import requests

class Requestor:
	"""Оператор запросов к нейросети."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __generate_in_thread(self, request: str, dictionary: dict, key: Any):
		"""
		Запускает генерацию в отдельном потоке.

		:param request: Текст запроса.
		:type request: str
		:param dictionary: Словарь, используемый в качестве контейнера ответов. Сюда будут записаны результаты генерации.
		:type dictionary: dict
		:param key: Ключ, под которым результат будет записан в словарь.
		:type key: Any
		"""

		Response = self.generate(request)
		dictionary[key] = Response

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, options: Options, host: str | None = None, port: int = 8000):
		"""
		Оператор запросов к нейросети.

		:param options: Опции генерации.
		:type options: Options
		:param host: Адрес хоста генерации. По умолчанию `127.0.0.1`.
		:type host: str | None, optional
		:param port: Номер порта. По умолчанию `8000`.
		:type port: int, optional
		"""

		self.__Options = options
		self.__Host = host
		self.__Port = port

		if not self.__Host: self.__Host = "127.0.0.1"
		
	def generate(self, request: str) -> WebResponse:
		"""
		Отправляет запрос на генерацию.

		:param request: Текст запроса.
		:type request: str
		:return: Контейнер ответа от сервера.
		:rtype: WebResponse
		"""

		Response = WebResponse()
		RequestData = self.__Options.to_dict()
		RequestData["request"] = request

		try:
			RequestsResponse = requests.post(f"http://{self.__Host}:{self.__Port}/generate", json = RequestData, timeout = self.__Options.timeout)
			Response.parse_response(RequestsResponse)

		except: pass

		return Response

	def start_thread_generation(self, request: str, dictionary: dict, key: Any):
		"""
		Запускает генерацию в отдельном потоке.

		:param request: Текст запроса.
		:type request: str
		:param dictionary: Словарь, используемый в качестве контейнера ответов. Сюда будут записаны результаты генерации.
		:type dictionary: dict
		:param key: Ключ, под которым результат будет записан в словарь.
		:type key: Any
		"""

		Thread(target = self.__generate_in_thread, args = (request, dictionary, key)).start()

	def wait_thread_generation(self, dictionary: dict[Any, WebResponse | None], key: Any, sleep_time: float = 0.1) -> WebResponse:
		"""
		Ожидает результат генерации в потоке.

		:param dictionary: Словарь, используемый в качестве контейнера ответов.
		:type dictionary: dict
		:param key: Ключ, под которым результат должен быть записан в словарь.
		:type key: Any
		:param sleep_time: Время ожидания между проверками словаря в секундах. По умолчанию `0.1`.
 		:type sleep_time: float, optional
		:return: Контейнер ответа от сервера.
		:rtype: WebResponse
		"""

		StartTime = datetime.now()

		while True:
			if type(dictionary[key]) == WebResponse and dictionary[key].status_code == 200: return dictionary[key]
			DeltaTime = datetime.now() - StartTime
			if DeltaTime.total_seconds() > self.__Options.timeout: return dictionary[key]
			sleep(sleep_time)
