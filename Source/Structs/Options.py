from .Languages import Languages

from typing import Any, Literal

class Options:
	"""Опции генерации."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def force_proxy(self) -> bool:
		"""Состояние: нужно ли использовать для всех запросов случайный прокси."""

		return self.__ForceProxy

	@property
	def language(self) -> Languages | None:
		"""Код языка ответа по стандарту ISO 639-1."""

		return self.__Language

	@property
	def max_length(self) -> int | None:
		"""Максимальная длина ответа."""

		return self.__MaxLength

	@property
	def model(self) -> str | None:
		"""Используемая модель нейросети."""

		return self.__Model

	@property
	def only_plaint_text(self) -> bool:
		"""Состояние: требуется ли вернуть только чистый текст без HTML тегов."""

		return True
	
	@property
	def source(self) -> Literal["gpt4free", "gemini"]:
		"""Источник нейросети."""

		return self.__Source

	@property
	def timeout(self) -> int:
		"""Время ожидания ответа."""

		return self.__Timeout

	@property
	def tries(self) -> int:
		"""Количество попыток получения валидного ответа."""

		return self.__Tries

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Опции генерации."""

		self.__Source: Literal["gpt4free", "gemini"] = "gpt4free"
		self.__Language: Languages | None = None
		self.__MaxLength: int | None = None
		self.__Timeout: int = 30
		self.__Tries = 3
		self.__Model = None
		self.__ForceProxy = False

	def select_source(self, source: Literal["gpt4free", "gemini"]):
		"""
		Выбирает генератор контента.

		:param source: Источник нейросети.
		:type source: Literal["gpt4free", "gemini"]
		"""

		if source not in ("gpt4free", "gemini"): raise Exception(f"Source \"{source}\" not found.")

		self.__Source = source

	def set_force_proxy(self, status: bool | None):
		"""
		Переключает использование прокси для всех запросов.

		:param status: Статус использования прокси. По умолчанию `False`, что соответствует использованию прокси только в случае блокировки запроса.
		:type status: bool | None
		"""

		self.__ForceProxy = bool(status)

	def set_language(self, language: Languages | str | None):
		"""
		Зазадёт код языка ответа по стандарту ISO 639-1.

		:param language: Двухсимвольный код языка ответа по стандарту ISO 639-1 или `None` для пропуска валидации языка.
		:type language: str | None
		"""

		if type(language) == str:
			if len(language) != 2: raise ValueError("ISO 639-1 requires two characters.")
			language = Languages(language)

		self.__Language = language

	def set_max_length(self, length: int | None):
		"""
		Зазадёт максимальную длину ответа.

		:param length: Длина ответа в символах Unicode.
		:type length: int | None
		"""

		self.__MaxLength = length

	def set_model(self, model: str | None):
		"""
		Зазадёт используемую модель.

		:param model: Название модели. Полный список для `g4f` [здесь](https://github.com/gpt4free/gpt4free.github.io/blob/main/docs%2Fproviders-and-models.md), для `gemini` [тут](https://ai.google.dev/gemini-api/docs/models).
		:type model: str | None
		"""

		self.__Model = model

	def set_timeout(self, timeout: int | None):
		"""
		Задаёт тайм-аут генерации ответа.

		:param timeout: Тайм-аут в секундах. При указании `None` используется значение по умолчанию: 30.
		:type timeout: int | None
		"""

		if not timeout: timeout = 30
		self.__Timeout = timeout

	def set_tries(self, tries: int | None):
		"""
		Задаёт количество попыток получения валидного ответа.

		:param tries: Количество попыток. При указании `None` используется значение по умолчанию: 3.
		:type tries: int | None
		"""

		if not tries: tries = 3
		self.__Tries = tries

	def to_dict(self) -> dict[str, Any]:
		"""
		Возвращает опции в виде словаря.

		:return: Словарь в формате, подходящем для отправки запроса генерации, без ключа _request_.
		:rtype: dict[str, Any]
		"""

		OptionsDict = {
			"proxy": self.__ForceProxy,
			"language": self.__Language.value if self.__Language else None,
			"length": self.__MaxLength,
			"timeout": self.__Timeout,
		}

		for Key in tuple(OptionsDict.keys()):
			if not OptionsDict[Key]: del OptionsDict[Key]

		return OptionsDict