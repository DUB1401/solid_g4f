import signal

def generate_with_timeout(self, request: str, timeout: Options) -> Response:
	"""
	Генерирует ответ нейросети и обрабатывает таймаут генерации. Может использоваться только из главного потока процесса.

	:param request: Текст запроса.
	:type request: str
	:param options: Опции генерации.
	:type options: Options
	:return: Контейнер ответа нейросети.
	:rtype: Response
	"""

	CurrentResponse = Response()
	signal.signal(signal.SIGALRM, self.__RaiseTimeoutException)
	signal.alarm(options.timeout)

	try: CurrentResponse = self.generate(request, options)
	except TimeoutException as ExceptionData: CurrentResponse.push_error(Errors.TimeoutReached)

	signal.alarm(0)

	return CurrentResponse