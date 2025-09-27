from .Errors import Errors
from typing import Any

import time

class Response:
	"""Контейнер ответа нейросети."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def text(self) -> str | None:
		"""Текст ответа нейросети."""

		return self.__Text
	
	@property
	def current_try(self) -> int:
		"""Номер текущей попытки генерации."""

		return self.__CurrentTry

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""
		Контейнер ответа нейросети.

		:param text: Текст ответа. По умолчанию 'None'.
		:type text: str | None, optional
		"""

		self.__Text = None
		self.__Time = None
		self.__CurrentTry = 1
		self.__ErrorsCounter = dict()
		self.__Messages = list()

		self.__StartTime = time.perf_counter()

	def __str__(self) -> str:
		"""Возвращает строковое представление ответа нейросети."""

		return str(self.to_dict())

	def get_error_count(self, error: Errors) -> int:
		"""
		Возвращает количество ошибок определённого типа.

		:param error: Тип ошибки.
		:type error: Errors
		:return: Количество ошибок данного типа.
		:rtype: int
		"""

		Count = 0

		try: Count = self.__ErrorsCounter[error.value]
		except KeyError: pass

		return Count

	def increment_try(self):
		"""Инкрементирует номер попытки генерации."""

		self.__CurrentTry += 1

	def push_error(self, error: Errors):
		"""
		Добавляет ошибку в счётчик.

		:param error: Тип ошибки.
		:type error: Errors
		"""

		if error.value not in self.__ErrorsCounter.keys(): self.__ErrorsCounter[error.value] = 1
		else: self.__ErrorsCounter[error.value] = self.__ErrorsCounter[error.value] + 1

	def push_message(self, message: str):
		"""
		Добавляет сообщение в сведения отладки.

		:param message: Текст сообщения.
		:type message: str
		"""

		self.__Messages.append(message)
		self.__Messages = list(set(self.__Messages))

	def set_text(self, text: str):
		"""
		Задаёт текст ответа.

		:param text: Текст ответа.
		:type text: str
		"""

		self.__Text = text

	def set_try(self, current_try: int):
		"""
		Инкрементирует номер попытки.

		:param current_try: Номер текущей попытки. генерации
		:type current_try: int
		"""

		self.__CurrentTry = current_try

	def stop_timer(self):
		"""Останавливает таймер выполнения и сохраняет значение."""

		self.__Time = round(time.perf_counter() - self.__StartTime, 2)

	def to_dict(self) -> dict[str, Any]:
		"""
		Возвращает словарное представление ответа.

		:return: Словарное представление ответа.
		:rtype: dict
		"""

		return {
			"text": self.__Text,
			"debug": {
				"time": self.__Time,
				"tries": self.__CurrentTry,
				"errors": self.__ErrorsCounter,
				"messages": self.__Messages
			}
		}