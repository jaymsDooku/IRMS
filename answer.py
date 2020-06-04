class Answer:

	def __init__(self, question, answerer, content):
		self.question = question
		self.answerer = answerer
		self.content = content

	def to_sql(self):
		return (self.question.id, self.answerer.id, self.content)