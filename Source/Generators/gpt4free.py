from Source.Structs import Options, Languages, Response, Errors
from Source.Generators.Base import BaseGenerator

from dublib.Polyglot import HTML

import logging
import random
import re

from g4f.client import Client
from g4f import errors

class Generator(BaseGenerator):
	"""Обработчик запросов к нейросетям."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ВАЛИДАЦИИ <<<<< #
	#==========================================================================================#

	def __IsRussian(self, text: str) -> bool:
		"""
		Проверяет валидность текста на основе регулярного выражения, исключающего латиницу и иные не кирилические символы.
		  text – проверяемый текст.
		"""

		return bool(re.match(r"^[А-Яа-яЁё\s.,:;!?()\-\–«»\"\'\[\]{}]+$", text, re.IGNORECASE))
	
	def __ValidateText(self, text: str | None, options: Options) -> str | Errors:
		"""
		Обрабатывает текст согласно параметрам и проводит его отбраковку.

		:param text: Обрабатываемый текст.
		:type text: str
		:param options: Опции генерации.
		:type options: Options
		:return: Обработанный текст или тип ошибки.
		:rtype: str | Errors
		"""

		if not text: return Errors.EmptyResponse

		if options.only_plaint_text: text = HTML(text).plain_text

		if options.max_length and len(text) > options.max_length: return Errors.MaxLengthExceeded
		if options.language and options.language == Languages.Russian and not self.__IsRussian(text): return Errors.IncorrectResponseLanguage

		if text in (
			"You have reached your request limit for the hour.",
			"502 Bad Gateway\nUnable to reach the origin service. The service may be down or it may not be responding to traffic from cloudflared"
		): return Errors.RequestBlocked

		return text

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _PostInitMethod(self):
		"""Метод, выполняющийся после инициализации объекта. Служит для переопределения."""

		self.__Client = Client()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

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

		while CurrentResponse.current_try <= options.tries and not CurrentResponse.text:
			
			if self._Proxies: 
				if CurrentResponse.get_error_count(Errors.RequestBlocked) or options.force_proxy:
					self.__Client = Client(proxies = random.choice(self._Proxies).to_dict())

			try:
				ResponseData = self.__Client.chat.completions.create(
					model = options.model,
					messages = [{"role": "user", "content": request}]
				)
				ValidatedData = self.__ValidateText(ResponseData.choices[0].message.content.strip(), options)

				if type(ValidatedData) == str:
					CurrentResponse.set_text(ValidatedData)
					break

				else: CurrentResponse.push_error(ValidatedData)

			except KeyboardInterrupt: break
			except (errors.MissingAuthError, errors.NoValidHarFileError): pass
			except Exception as ExceptionData:
				logging.error(str(ExceptionData))
				CurrentResponse.push_message(str(ExceptionData))

			CurrentResponse.increment_try()

		if CurrentResponse.current_try > options.tries: CurrentResponse.set_try(options.tries)
		CurrentResponse.stop_timer()
		
		return CurrentResponse