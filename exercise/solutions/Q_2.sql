CREATE OR REPLACE FUNCTION genres_movie(input_genre varchar) 
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
			select .
				genres.genre_id 
			from genres 
			where genres.name ILIKE input_genre);
END; $$
LANGUAGE 'plpgsql';