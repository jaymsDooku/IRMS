from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__, static_url_path='/static', instance_relative_config=True)

@app.route('/')
def user_page():
	return render_template('irms.html')

app.run()