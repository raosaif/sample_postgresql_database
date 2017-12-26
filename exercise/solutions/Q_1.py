from postgresql_api import *

api_handle = postgresql_api()
cur = api_handle.connect_db()

cur.execute('''CREATE OR REPLACE FUNCTION movie_details(input_id integer) 
RETURNS TABLE (
    content_id integer,
    title varchar,
    description text,
    total_seasons integer,
    imdb_score decimal,
    release_dates varchar,
    total_episodes integer,
    imdb_link varchar
    )
AS $$
BEGIN
RETURN QUERY SELECT 
contents.content_id,
contents.title,
contents.description,
contents.total_seasons,
contents.imdb_score,
contents.release_dates,
contents.total_episodes,
contents.imdb_link 
FROM contents
WHERE contents.content_id = input_id;
END; $$
LANGUAGE 'plpgsql';''')

api_handle.commit_api()

cur.callproc('movie_details', (1,))
	# process the result set
row = cur.fetchone()
while row is not None:
	print(row)
	row = cur.fetchone()

api_handle.close_api()
