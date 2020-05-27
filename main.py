from flask import Flask

app = Flask(__name__, static_url_path='/static', instance_relative_config=True)

@app.route('/')
def user_page():
	return 'Hello world!'

app.run()