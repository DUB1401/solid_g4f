from .gpt4free import Generator as g4f

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..Structs.Response import Response
	from ..Structs.Options import Options

def Generate(request: str, options: "Options") -> "Response":
	"""
	Генерирует контент по запросу.

	:param request: Запрос.
	:type request: str
	:param options: Опции запроса.
	:type options: Options
	:return: Ответ генератора.
	:rtype: Response
	"""

	Generator = None

	match options.source:
		case "g4f": Generator = g4f()

	return Generator.generate(request, options)