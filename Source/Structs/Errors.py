import enum

class Errors(enum.Enum):
	"""Перечисление ошибок генерации."""

	MaxLengthExceeded = "max_length_exceeded"
	EmptyResponse = "empty_response"
	IncorrectResponseLanguage = "incorrect_response_language"
	RequestBlocked = "request_blocked"
	RateLimit = "rate_limit"
	TimeoutReached = "timeout_reached"
	SourceNotFound = "source_not_found"
	RequestError = "request_error"