from Source.Structs import Options, Response

from dublib.Methods.Filesystem import ReadTextFile
from dublib.WebRequestor import Proxy

import os

class BaseGenerator:
	"""Шаблон обработчика запросов к нейросетям."""
	
	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	def proxies(self) -> tuple[Proxy]:
		"""Набор данных прокси-серверов."""

		return self.__Proxies

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _ReadProxies(self):
		"""Считывает данные прокси из файла `Proxies.txt`."""

		Proxies = list()

		if os.path.exists("Proxies.txt"):
			Data = ReadTextFile("Proxies.txt", split = True)

			for Line in Data: 
				if Line: Proxies.append(Proxy().parse(Line))

		self._Proxies = tuple(Proxies)

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _PostInitMethod(self):
		"""Метод, выполняющийся после инициализации объекта. Служит для переопределения."""

		pass

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Шаблон обработчика запросов к нейросетям."""

		self._Proxies: tuple[Proxy] = tuple()

		self._ReadProxies()
		self._PostInitMethod()

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

		pass