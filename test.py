from database import Database
from entity_manager import EntityManager

db = Database('test.db')

def first_time():
	print('THIS IS THE FIRST TIME')

db.connect(first_time)

def execute_script(filename):
	script = open(filename, "r")
	queries = db.parse_queries(script)
	db.execute_queries(queries)
	script.close()

execute_script("SQL_scripts/drop_tables.sql")
execute_script("SQL_scripts/create_tables.sql")

em = EntityManager(db)

role = em.create_role("Service Desk", True)
user = em.create_user("Joe", "Biden", "JB@email.com", role)
department = em.create_department("General Management")
team = em.create_team("Marketing", department)

em.dump()

db.commit()

db.close()