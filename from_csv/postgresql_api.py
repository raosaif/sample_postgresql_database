import psycopg2
from datetime import datetime
import json
import ast

class postgresql_api:

	def __init__(self):
		conn = ''
		cur = ''

	def __str__(self):
		return 'in_movies'

	def connect_db(self,dbname='imdb',user='username',host='localhost',password='password'):

		connect_str = ('dbname={} user={} host={} password={}'.format(dbname,user,host,password))
		print ("Connecting to database --->{}".format( connect_str))

		self.conn = psycopg2.connect(connect_str)
		self.cur = self.conn.cursor()

	def commit_api(self):
		pass
		self.conn.commit()

	def is_show_exisits(self,title,release_dates):
		isShowExist = None
		self.cur.execute("SELECT content_id from contents where title = %s and release_dates = %s;",(title,release_dates))
		isShowExist = self.cur.fetchone()
		return isShowExist

	def get_language_array(self,languages_list):
		positions= []
		positions.append(0)
		for pos ,char in enumerate(languages_list):
			if(char == ','):
				positions.append(pos)
		positions.append(len(languages_list))
		
		languages=[]
		for lan in range(1,len(positions)):
			first = positions[lan-1]
			second = positions[lan]
			languages.append(languages_list[first:second].replace(', ',''))

		return languages

	def insert_content_data(self,content_data):
		temp = content_data[13]
		json_temp = ast.literal_eval(temp)
		content_rating = 0
		if content_data[7] == '':
				content_rating = 1
		else:
			content_rating = int(content_data[7]),	# content_rating

		if(self.is_show_exisits(content_data[1],content_data[5]) == None):
			self.cur.execute('''INSERT INTO contents (title,languages,release_dates,imdb_link,play_time,content_type,content_rating,
				description,total_seasons,imdb_score,imdb_score_votes,total_episodes,rating_details,last_updated)
				VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())''', (
				content_data[1], # title
				self.get_language_array((content_data[14].strip('[]')).replace("'","")), # languages
				content_data[5], #release_dates
				content_data[10], # imdb_link
				content_data[6], # play_time
				int(content_data[9]), # content_type
				content_rating,
				content_data[2], # description
				int(content_data[3]), # total_seasons
				float(content_data[4]), # imdb_score
				int(content_data[12]), # imdb_Score_votes
				int(content_data[8]),  # total_episodes
				json.dumps(json_temp),
				))

			print("Index:-----New Data Inserted: ", content_data[1])
		else:
			print("Already Exist: ", content_data[1])

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
		self.cur.execute('''INSERT INTO episode_list (episode_imdb_link,description,episode_num,season_num,
			episode_name,content_id,release_date,episode_rating,episode_score_votes,last_updated)
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,now())''', (
		episodes_dict[9],   #['episode_imdb_link'],
		episodes_dict[7],   #['episode_description'],
		int(episodes_dict[6]),   #['episode_num'],
		int(episodes_dict[1]),   #['season_num'],
		episodes_dict[2],   #['episode_name'],
		int(episodes_dict[3]),   #['content_id']
		episodes_dict[4],   #['release_date'],
		float(episodes_dict[5]),   #['episode_rating'],
		int(episodes_dict[10]),  #['episode_score_votes'],
		))
		print("INSERTED: Title: ",episodes_dict[9])

	def insert_languages(self,language):
		self.cur.execute("SELECT language_id from languages where name = %s;",(language[1],))
		isLanguageExists = self.cur.fetchone()
		#print('Languages: ', isLanguageExists)
		if(isLanguageExists == None):
			self.cur.execute('''INSERT INTO languages (name,last_updated)
					VALUES (%s,now())''', (
					language[1],
					))

			print("Entered New Language in DB: ", language[1])

	def insert_content_genres(self,content_data):
		genre_id = 0
		if(content_data[0] == ''):
			self.cur.execute('''INSERT INTO content_genres (content_id,last_updated)
					VALUES (%s,now())''', (
					int(content_data[1]),
					))
		else:
			genre_id = int(content_data[0])
			self.cur.execute('''INSERT INTO content_genres (genre_id,content_id,last_updated)
						VALUES (%s,%s,now())''', (
						genre_id,
						int(content_data[1]),
						))
		print("Updated Genre")

	def insert_actors(self,content_data):
		self.cur.execute('''INSERT INTO actors (name,last_updated)
						VALUES (%s,now())''', (
						content_data[1],
						))
		print("Actor Added in DB : ", content_data[1])


	def insert_content_actors(self,content_data):
		self.cur.execute('''INSERT INTO content_actors (actor_id,content_id,last_updated)
					VALUES (%s,%s,now())''', (
					int(content_data[0]),
					int(content_data[1]),
					))
		print("Actors Added: ", content_data[0] )

	def insert_content_directors(self,content_data):
		self.cur.execute('''INSERT INTO content_directors (director_id,content_id,last_updated)
				VALUES (%s,%s,now())''', (
				content_data[0],
				content_data[1],
				))
		print("Directors Added:: ", content_data[0])

	def insert_directors(self,content_data):
		self.cur.execute('''INSERT INTO directors (name,last_updated)
						VALUES (%s,now())''', (
						content_data[1],
						))
		print("New Director Added in DB : ", content_data[1])


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
	def close_api(self):
		self.cur.close()
		self.conn.close()
