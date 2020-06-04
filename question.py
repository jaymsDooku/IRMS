class Question:

	def __init__(self, title, author, content):
		self.title = title
		self.author = author
		self.content = content
		self.answers = []

	def count_answers(self):
		return len(self.answers)

	def to_sql(self):
		return (self.title, self.author.id, self.question)