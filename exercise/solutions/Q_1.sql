CREATE OR REPLACE FUNCTION movie_details(input_id integer) 
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
LANGUAGE 'plpgsql';
    