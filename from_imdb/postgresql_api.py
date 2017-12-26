import psycopg2
from psycopg2 import sql
from datetime import datetime
import json

class postgresql_api:

	
	def __init__(self):
		conn = ''
		cur = ''

	def __str__(self):
		return 'in_movies'

	def connect_db(self,dbname='imdb',user='username',host='localhost',password='password'):

		connect_str = ('dbname={} user={} host={} password={}'.format(dbname,user,host,password))
		print ("Connecting to database: {}".format( connect_str))

		self.conn = psycopg2.connect(connect_str)
		self.cur = self.conn.cursor()

	def commit_api(self):
		pass
		self.conn.commit()

	def insert_languages(self,languages):
		isLanguageExists = None
		for lan in range(len(languages)):
			self.cur.execute("SELECT language_id from languages where name = %s;",(languages[lan],))
			isLanguageExists = self.cur.fetchone()
			#print('Languages: ', isLanguageExists)
			if(isLanguageExists == None):
				self.cur.execute('''INSERT INTO languages (name,last_updated)
						VALUES (%s,now())''', (
						languages[lan],
						))

				print("Entered New Language in DB: ", languages[lan])


	def insert_genres_contents(self,content_data):
		self.cur.execute("SELECT content_id from contents where title = %s and release_dates = %s;",(content_data['title'],content_data['release_dates']))
		content_id = self.cur.fetchone()

		for gen in range(len(content_data['genre'])):
			self.cur.execute("SELECT genre_id from genres where genres.name = %s;",(content_data['genre'][gen],))
			genre_id = self.cur.fetchone()

			self.cur.execute('''INSERT INTO content_genres (genre_id,content_id,last_updated)
						VALUES (%s,%s,now())''', (
						genre_id,
						content_id,
						))
		print("Updated Genre also for : ", content_data.get('title'))

	def insert_actors_contents(self,content_data):
		self.cur.execute("SELECT content_id from contents where title = %s and release_dates = %s;",(content_data['title'],content_data['release_dates']))
		content_id = self.cur.fetchone()

		for actor in range(len(content_data['cast'])):
			self.cur.execute("SELECT actor_id from actors where actors.name = %s;",(content_data['cast'][actor],))
			actor_id = self.cur.fetchone()

			self.cur.execute('''INSERT INTO content_actors (actor_id,content_id,last_updated)
						VALUES (%s,%s,now())''', (
						actor_id,
						content_id,
						))
		print("Actors Added for respective Show : ", content_data.get('title'))

	def insert_actors(self,actors_list):
		for actor in range(len(actors_list)):
			actor_name = None
			self.cur.execute("SELECT name from actors where name = %s;",(actors_list[actor],))
			actor_name = self.cur.fetchone()

			if(actor_name == None):
				#print(actors_list[actor])
				self.cur.execute('''INSERT INTO actors (name,last_updated)
								VALUES (%s,now())''', (
								actors_list[actor],
								))
				print("New Actor Added in DB : ", actors_list[actor])
			else:
				print('Actors Information Exists')

	def insert_directors_contents(self,content_data):
		self.cur.execute("SELECT content_id from contents where title = %s and release_dates = %s;",(content_data['title'],content_data['release_dates']))
		content_id = self.cur.fetchone()

		for director in range(len(content_data['directors'])):
			self.cur.execute("SELECT director_id from directors where directors.name = %s;",(content_data['directors'][director],))
			director_id = self.cur.fetchone()

			self.cur.execute('''INSERT INTO content_directors (director_id,content_id,last_updated)
						VALUES (%s,%s,now())''', (
						director_id,
						content_id,
						))
		print("Directors Added for respective Show : ", content_data.get('title'))

	def insert_directors(self,directors_list):
		for director in range(len(directors_list)):
			director_name = None
			self.cur.execute("SELECT name from directors where name = %s;",(directors_list[director],))
			director_name = self.cur.fetchone()

			if(director_name == None):
				#print(directors_list[director])
				self.cur.execute('''INSERT INTO directors (name,last_updated)
								VALUES (%s,now())''', (
								directors_list[director],
								))
				print("New Director Added in DB : ", directors_list[director])
			else:
				print('Directors Information exists')

	def insert_content_data(self,content_data,content_type):
		#print (json.dumps(content_data,indent=4))
		#print('IN API: ', type(json.dumps(content_data['rating_details'])))
		#print("*"* 60)
		#print(json.dumps(content_data['rating_details']))
		content_id = 0
		to_search_content = ''
		if(content_type == 'M'):
			to_search_content = 'Movie'
		elif(content_type == 'T'):
			to_search_content = 'TV-Series'
		elif(content_type == 'D'): 
			to_search_content= 'Documentary'

		current_genre = []
		

		self.cur.execute("SELECT content_type_id from content_types where name=%s;",(to_search_content,))
		content_id = self.cur.fetchone()

		self.cur.execute("SELECT content_rating_id from content_ratings where name = %s;",(content_data['content_rating'],))
		db_content_rating = self.cur.fetchone()

		#print(content_id)
		#print(db_content_rating)

		isShowExist = None
		self.cur.execute("SELECT title,release_dates,content_id from contents where title = %s and release_dates = %s;",(content_data['title'],content_data['release_dates']))
		isShowExist = self.cur.fetchone()
		#print('Is Show Exists',isShowExist)
		if(isShowExist == None):
			self.cur.execute('''INSERT INTO contents (title,release_dates,imdb_link,play_time,content_type,content_rating,
				description,total_seasons,imdb_score,imdb_score_votes,total_episodes,languages,rating_details,last_updated)
				VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())''', (
				content_data['title'],
				content_data['release_dates'],
				content_data['imdb_link'],
				content_data['play_time'],
				content_id,
				db_content_rating,
				content_data['description'],
				content_data['total_seasons'],
				content_data['overall_rating'],
				content_data['imdb_score_votes'],
				content_data['total_episodes'],
				content_data['languages'],
				json.dumps(content_data['rating_details']),
				))

			print("New Data Inserted: ", content_data.get('title'))

			self.insert_genres_contents(content_data)
			self.insert_actors_contents(content_data)
			self.insert_directors_contents(content_data)
			return True
		else:
			print("TV Show: ",content_data['title']," Already Exists in DB")
			return False

	
	def is_show_exisits(self,content_data):
		isShowExist = None
		self.cur.execute("SELECT content_id from contents where title = %s and release_dates = %s;",(content_data['title'],content_data['release_dates']))
		isShowExist = self.cur.fetchone()
		return isShowExist

	def is_episode_not_exists(self,episodes_dict):
		if(self.is_show_exisits(episodes_dict)):
			isEpisodeExist = None
			self.cur.execute('''SELECT episode_name,content_id from episode_list
				where episode_name = %s and content_id = %s;''',
				(episodes_dict['episode_name'],self.is_show_exisits(episodes_dict)))

			isEpisodeExist = self.cur.fetchone()
			#print('Episode: ',isEpisodeExist)

			if(isEpisodeExist == None):
				return True
			else:
				return False
		else:
			False

	def insert_episodes(self,episodes_dict):
		isShowExists = self.is_show_exisits(episodes_dict)
		#print(isShowExists)

		if(self.is_episode_not_exists or isShowExists):
			self.cur.execute('''INSERT INTO episode_list (episode_imdb_link,description,episode_num,season_num,
				episode_name,content_id,release_date,episode_rating,episode_score_votes,last_updated)
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,now())''', (
			episodes_dict['episode_imdb_link'],
			episodes_dict['episode_description'],
			episodes_dict['episode_num']+1,
			episodes_dict['season_num']+1,
			episodes_dict['episode_name'],
			isShowExists,
			episodes_dict['release_date'],
			episodes_dict['episode_rating'],
			episodes_dict['episode_score_votes'],
			))

			print("INSERTED: Title: ",episodes_dict['title'],"Episode Name: ",episodes_dict['episode_name'], ', season num: ',episodes_dict['season_num']+1,' and episode num:', episodes_dict['episode_num']+1)
			return True
		else:
			print("Episode Information Already Exists")
			return False

	def updating_total_episodes(self,content_data):
		isShowExists = None
		isShowExists = self.is_show_exisits(content_data)
		#print(isShowExists, content_data['total_episodes'])
		if(isShowExists):
			self.cur.execute('UPDATE contents SET total_episodes = %s where content_id = %s',(content_data['total_episodes'],isShowExists))


	def create_tables(self):
		now = datetime.now().isoformat()

		##############################################################################################

		self.cur.execute('''CREATE TABLE content_types(
		content_type_id serial PRIMARY KEY,
		name varchar(250) NOT NULL UNIQUE,
		last_updated timestamp);''')


		rows = (('TV-Series',now),('Movie',now),('Documentary',now),('Biography',now),('Animation',now))
		dataText = b','.join(self.cur.mogrify("(%s,%s)",row) for row in rows)
		self.cur.execute(b"INSERT INTO content_types(name,last_updated) VALUES " + dataText)

		print('[LOG] content_types table created successfully with default data!')
		##############################################################################################

		self.cur.execute(''' CREATE TABLE content_ratings(
		content_rating_id serial PRIMARY KEY,
		content_type_id integer references content_types(content_type_id),
		name varchar(250) NOT NULL UNIQUE,
		description text,
		last_updated timestamp);''')

		rows = ((1,'TV-Y','This program is designed to be appropriate for all children.',now),
		(1,'TV-Y7','This program is designed for children age 7 and above.',now),
		(1,'TV-G','Programs suitable for all ages.',now),
		(1,'TV-PG','This program contains material that parents may find unsuitable for younger children.',now),
		(1,'TV-14','This program contains some material that many parents would find unsuitable for children under 14 years of age.',now),
		(1,'TV-MA','This program is specifically designed to be viewed by adults and therefore may be unsuitable for children under 17.',now),
		(2,'G',' General Audiences-All ages admitted. Nothing that would offend parents for viewing by children.',now),
		(2,'PG','Parental Guidance Suggested-Some material may not be suitable for children. Parents urged to give "parental guidance". May contain some material parents might not like for their young children.',now),
		(2,'PG-13','Parents Strongly Cautioned-Some material may be inappropriate for children under 13. Parents are urged to be cautious. Some material may be inappropriate for pre-teenagers.',now),
		(2,'R',' Restricted-Under 17 requires accompanying parent or adult guardian. Contains some adult material. Parents are urged to learn more about the film before taking their young children with them.',now),
		(2,'NC-17','Adults Only-No One 17 and Under Admitted. Clearly adult. Children are not admitted.',now))

		dataText = b','.join(self.cur.mogrify("(%s,%s,%s,%s)",row) for row in rows)
		self.cur.execute(b"INSERT INTO content_ratings(content_type_id,name,description,last_updated) VALUES " + dataText)

		print('[LOG] content_ratings table created successfully with default data!')
		###############################################################################################

		self.cur.execute('''CREATE TABLE contents
		(content_id serial PRIMARY KEY,
		title varchar NOT NULL,
		description text,
		total_seasons integer NOT NULL,
		imdb_score decimal NOT NULL,
		release_dates varchar(250) NOT NULL,
		play_time varchar(250) NOT NULL,
		content_rating integer references content_ratings(content_rating_id),
		total_episodes integer NOT NULL,
		content_type integer references content_types(content_type_id) NOT NULL,
		imdb_link varchar(250) NOT NULL UNIQUE,
		last_updated timestamp NOT NULL,
		imdb_score_votes integer NOT NULL DEFAULT 0,
		rating_details json NOT NULL DEFAULT '{}',
		languages varchar(50)[] NOT NULL
		);''')

		print('[LOG] contents table created successfully!')
		################################################################################################

		self.cur.execute('''CREATE TABLE episode_list
		(episode_id serial PRIMARY KEY,
		season_num integer NOT NULL,
		episode_name varchar(250) NOT NULL,
		content_id integer REFERENCES contents(content_id),
		release_date varchar(250) NOT NULL,
		episode_rating decimal NOT NULL,
		episode_num integer NOT NULL,
		description text,
		last_updated timestamp NOT NULL,
		episode_imdb_link varchar (250) NOT NULL UNIQUE,
		episode_score_votes integer NOT NULL
		);''')

		print('[LOG] episode_list table created successfully!')
		#################################################################################################

		self.cur.execute(''' CREATE TABLE genres
		(genre_id serial PRIMARY KEY,
		name varchar(250) NOT NULL UNIQUE,
		last_updated timestamp NOT NULL );''')

		self.cur.execute("INSERT INTO genres(name,last_updated) VALUES ('Action',now()),('Animation',now()),('Adventure',now()),('Biography',now()) ,('Comedy',now()) ," + \
		"('Crime',now()),('Documentary',now()),('Drama',now()),('Family',now()),('Fantasy',now()) ," + \
		"('Film-Noir',now()),('History',now()),('Horror',now()),('Music',now()),('Musical',now()) ," +\
		"('Mystery',now()),('Romance',now()),('Sci-Fi',now()),('Sport',now()),('Thriller',now()), ('War',now()), ('Western',now())")

		print('[LOG] genre table created successfully with default data!')

		##################################################################################################
		self.cur.execute(''' CREATE TABLE content_genres(
		genre_id integer references genres,
		content_id integer references contents,
		last_updated timestamp);''')

		print('[LOG] content_genres table created successfully!')

		##################################################################################################

		self.cur.execute(''' CREATE TABLE actors
		(actor_id serial PRIMARY KEY,
		name varchar(250) NOT NULL,
		last_updated timestamp NOT NULL );''')

		print('[LOG] actors table created successfully!')

		###################################################################################################

		self.cur.execute(''' CREATE TABLE content_actors(
		actor_id integer references actors,
		content_id integer references contents,
		last_updated timestamp);''')

		print('[LOG] content_actors table created successfully!')

		####################################################################################################

		self.cur.execute(''' CREATE TABLE directors
		(director_id serial PRIMARY KEY,
		name varchar(250) NOT NULL,
		last_updated timestamp NOT NULL );''')

		print('[LOG] directors table created successfully!')

		# ##################################################################################################

		self.cur.execute(''' CREATE TABLE content_directors(
		director_id integer references directors,
		content_id integer references contents,
		last_updated timestamp);''')

		print('[LOG] content_directors table created successfully!')

		#####################################################################################################

		self.cur.execute(''' CREATE TABLE languages
		(language_id serial PRIMARY KEY,
		name varchar(250) NOT NULL UNIQUE,
		last_updated timestamp NOT NULL );''')

		print('[LOG] languages table created successfully!')

		######################################################################################################

	def close(self):
		self.cur.close()
		self.conn.close()