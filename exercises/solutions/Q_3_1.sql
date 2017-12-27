SELECT * from contents 
where content_rating = (
	select content_rating_id from content_ratings 
	where name ILIKE 'TV-MA'
	);