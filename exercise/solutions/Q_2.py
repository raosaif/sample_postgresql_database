import psycopg2

connect_str = "dbname='imdb_restore' user='rao' host='localhost' " + \
                  "password='raoali'"
    # use our connection values to establish a connection

# Connect to an existing database
conn = psycopg2.connect(connect_str)

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('''CREATE OR REPLACE FUNCTION genres_movie(input_genre varchar) 
RETURNS TABLE (
    content_id integer,
    title varchar,
    genre_id integer,
    genre varchar
    )
AS $$
BEGIN
RETURN QUERY 
SELECT 
    contents.content_id,
    contents.title, 
    content_genres.
    genre_id, 
    input_genre

FROM contents
INNER JOIN content_genres ON content_genres.content_id = contents.content_id 
WHERE 
    content_genres.genre_id = (
            select 
                genres.genre_id 
            from genres 
            where genres.name ILIKE input_genre);
END; $$
LANGUAGE 'plpgsql';''')

conn.commit()

cur.callproc('genres_movie', ('Comedy',))
	# process the result set
row = cur.fetchone()

while row is not None:
	print(row)
	row = cur.fetchone()

print('Total Rows: ',cur.rowcount)
cur.close()
conn.close()
