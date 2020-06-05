from enum import Enum
from datetime import datetime

class TimeUnit(Enum):

	MILLISECOND = 1
	SECOND = 2
	MINUTE = 3
	HOUR = 4
	DAY = 5

class TimeUtil:

	@staticmethod
	def to_millis(time, unit):
		if unit == TimeUnit.SECOND:
			return time * 1000
		elif unit == TimeUnit.MINUTE:
			return time * 1000 * 60
		elif unit == TimeUnit.HOUR:
			return time * 1000 * 60 * 60
		elif unit == TimeUnit.DAY:
			return time * 1000 * 60 * 60 * 24

	@staticmethod
	def from_millis(millis):
		pass

	@staticmethod
	def to_datetime(input):
		datetime_obj = datetime.strptime(input, '%d-%m-%Y %H:%M:%S')
		return datetime_obj

	@staticmethod
	def sqlite_to_datetime(input):
		datetime_obj = datetime.strptime(input, '%Y-%m-%d %H:%M:%S')
		return datetime_obj

	@staticmethod
	def now():
		return datetime.now()

	@staticmethod
	def sanitize_time_input(input):
		result = ' '.join(input.split('T'))
		result += ':00'
		return result

	@staticmethod
	def datetime_to_string(date):
		return date.strftime("%Y-%m-%dT%H:%M")

	@staticmethod
	def desanitize_time_input(sanitized):
		result = sanitized[0:-3]
		result = 'T'.join(result.split(' '))
		return result