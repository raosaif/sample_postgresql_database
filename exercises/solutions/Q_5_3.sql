SELECT content_id, title, imdb_score_votes,
	case when (imdb_score_votes > (select AVG(imdb_Score_votes) from contents)) then 'ABOVE'
               else
               	'BELOW'
              end as Remarks
            from contents 
            Group by content_id 
            having imdb_score_votes < (select AVG(imdb_Score_votes) from contents)
            ORDER BY content_id ASC ;