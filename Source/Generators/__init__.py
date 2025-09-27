from ..Structs import Errors, Options, Response
from . import gpt4free
from . import gemini

def Generate(request: str, options: Options) -> Response:
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
	NeuroResponse = Response()
	NeuroResponse.push_error(Errors.SourceNotFound)

	match options.source:
		case "g4f": Generator = gpt4free.Generator()
		case "gemini": Generator = gemini.Generator()

	if Generator: NeuroResponse = Generator.generate(request, options)

	return NeuroResponse