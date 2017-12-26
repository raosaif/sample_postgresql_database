import psycopg2

class postgresql_api:

	
	def __init__(self):
		conn = ''
		cur = ''

	def __str__(self):
		return 'solutions'

	def connect_db(self):

		connect_str = "dbname='imdb' user='user' host='localhost' " + \
	              "password='password'"

		print ("Connecting to database: {}".format( connect_str))

		self.conn = psycopg2.connect(connect_str)
		self.cur = self.conn.cursor()

		return self.cur

	def commit_api(self):
		pass
		self.conn.commit()


	def close_api(self):
		self.cur.close()
		self.conn.close()
