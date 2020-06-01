from enum import Enum

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