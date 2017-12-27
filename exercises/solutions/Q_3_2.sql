SELECT * from contents 
INNER JOIN content_ratings ON content_ratings.content_Rating_id = contents.content_rating
where content_ratings.name ILIKE 'TV-MA';