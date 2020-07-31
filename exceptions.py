import copy, six
'''
Whole code is taken from google cloud sdk
'''

def _to_bytes(value, encoding='ascii'):
	"""Converts a string value to bytes, if necessary.

	Unfortunately, ``six.b`` is insufficient for this task since in
	Python2 it does not modify ``unicode`` objects.

	:type value: str / bytes or unicode
	:param value: The string/bytes value to be converted.

	:type encoding: str
	:param encoding: The encoding to use to convert unicode to bytes. Defaults
					 to "ascii", which will not allow any characters from
					 ordinals larger than 127. Other useful values are
					 "latin-1", which which will only allows byte ordinals
					 (up to 255) and "utf-8", which will encode any unicode
					 that needs to be.

	:rtype: str / bytes
	:returns: The original value converted to bytes (if unicode) or as passed
			  in if it started out as bytes.
	:raises TypeError: if the value could not be converted to bytes.
	"""
	result = (value.encode(encoding)
			  if isinstance(value, six.text_type) else value)
	if isinstance(result, six.binary_type):
		return result
	else:
		raise TypeError('%r could not be converted to bytes' % (value,))


class GoogleCloudError(Exception):
	"""Base error class for Google Cloud errors (abstract).

    Each subclass represents a single type of HTTP error response.
    """


	code = None
	"""HTTP status code.  Concrete subclasses *must* define.

	See: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
	"""


	def __init__(self, message, errors=()):
		super(GoogleCloudError, self).__init__(message)
		self.message = message
		self._errors = errors


	def __str__(self):
		result = u'%d %s' % (self.code, self.message)
		if six.PY2:
			result = _to_bytes(result, 'utf-8')
		return result


	@property
	def errors(self):
		"""Detailed error information.

		:rtype: list(dict)
		:returns: a list of mappings describing each error.
		"""
		return [copy.deepcopy(error) for error in self._errors]


class ClientError(GoogleCloudError):
	"""Base for 4xx responses

	This class is abstract
	"""


class Conflict(ClientError):
	"""Exception mapping a '409 Conflict' response."""
	code = 409
