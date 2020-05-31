from flask import json

from werkzeug.wrappers import BaseResponse as Response

class Util:

	MIMETYPE_HTML = 'text/html'
	MIMETYPE_JSON = 'application/json'

	@staticmethod
	def json_response(data, statusCode):
		return Response(response = json.dumps(data), 
			status = statusCode, 
			mimetype = Util.MIMETYPE_JSON)
