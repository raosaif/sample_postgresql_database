from postgresql_api import *
import csv

dir_path = './csv_files/'

all_files = ['contents.csv','episode_list.csv','languages.csv','content_genres.csv','actors.csv',
			'content_actors.csv','directors.csv','content_directors.csv']

api_handle = postgresql_api()
# default host is localhost and dbname is imdb

api_handle.connect_db(dbname='dbname',user='user',host='host',password='password')

api_handle.create_tables()
api_handle.commit_api()


for file in range(len(all_files)):
	rows = []
	csv_file_path = dir_path + all_files[file]
	print('Parsing: ',csv_file_path)
	with open(csv_file_path, "rt") as f_obj:
		reader = csv.reader(f_obj)
		for row in reader:
			rows.append(row)

	if 'contents' in all_files[file]:
		for index in range(1,len(rows)):
			api_handle.insert_content_data(rows[index])

	if 'episode_list' in all_files[file]:
		for index in range(1,len(rows)):
			api_handle.insert_episodes(rows[index])

	if 'languages' in all_files[file]:
		for index in range(1,len(rows)):
			api_handle.insert_languages(rows[index])

	if 'genres' in all_files[file]:
		for index in range(1,len(rows)):
			api_handle.insert_content_genres(rows[index])

	if 'actors' in all_files[file] and 'content' not in all_files[file]:
		for index in range(1,len(rows)):
			api_handle.insert_actors(rows[index])

	if 'content_actors' in all_files[file]:
		for index in range(1,len(rows)):
			api_handle.insert_content_actors(rows[index])

	if 'directors' in all_files[file] and 'content' not in all_files[file]:
		for index in range(1,len(rows)):
			api_handle.insert_directors(rows[index])

	if 'content_directors' in all_files[file]:
		for index in range(1,len(rows)):
			api_handle.insert_content_directors(rows[index])


api_handle.commit_api()
api_handle.close_api()
print('ALL DATA UPLOADED SUCCESSFULLY')
