from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__, static_url_path='/static', instance_relative_config=True)

database = Database('irms.db')
database.connect()

entity_manager = EntityManager(database)

@app.route('/')
def user_page():
	return render_template('irms.html')

app.run()