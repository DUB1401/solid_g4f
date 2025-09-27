from Source.Structs import Errors, Options, Response
from Source.Generators.Base import BaseGenerator

import logging
import random
import os

from google.genai import errors
from google import genai
import httpx

class Generator(BaseGenerator):
	"""Обработчик запросов к нейросетям."""

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _PostInitMethod(self):
		"""Метод, выполняющийся после инициализации объекта. Служит для переопределения."""

		self.__Client = genai.Client()

	def generate(self, request: str, options: Options) -> Response:
		"""
		Отправляет запрос на генерацию к источнику.

		:param request: Текст запроса.
		:type request: str
		:param options: Опции генерации.
		:type options: Options
		:return: Контейнер ответа нейросети.
		:rtype: Response
		"""

		CurrentResponse = Response()

		while CurrentResponse.current_try < options.tries and not CurrentResponse.text:
			CurrentResponse.increment_try()

			if self._Proxies: 
				if CurrentResponse.get_error_count(Errors.RequestBlocked) or options.force_proxy:
					CurrentProxy = random.choice(self._Proxies).to_string()
					os.environ["HTTPS_PROXY"] = CurrentProxy
					os.environ["HTTP_PROXY"] = CurrentProxy
					self.__Client = genai.Client()

			try:
				GeminiResponse = self.__Client.models.generate_content(
					model = options.model,
					contents = request
				)
				CurrentResponse.set_text(GeminiResponse.text)

			except httpx.ConnectError: CurrentResponse.push_error(Errors.RequestError)
			except errors.ClientError: CurrentResponse.push_error(Errors.RequestBlocked)
			except Exception as ExceptionData:
				logging.error(str(ExceptionData))
				CurrentResponse.push_message(str(ExceptionData))

		CurrentResponse.stop_timer()

		try:
			del os.environ["HTTPS_PROXY"]
			del os.environ["HTTP_PROXY"]

		except KeyError: pass

		return CurrentResponse