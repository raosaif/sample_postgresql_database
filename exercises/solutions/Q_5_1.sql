SELECT content_id, title, imdb_score_votes,
	case when (imdb_score_votes > (select AVG(imdb_Score_votes) from contents)) then 'ABOVE'
               else
               	'BELOW'
              end as Remarks
            from contents 
            Group by content_id 
            ORDER BY content_id ASC ;