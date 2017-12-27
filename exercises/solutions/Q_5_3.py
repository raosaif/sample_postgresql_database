
from postgresql_api import *


api_handle = postgresql_api()
cur = api_handle.connect_db()

cur.execute('''SELECT content_id, title, imdb_score_votes,
	case when (imdb_score_votes > (select AVG(imdb_Score_votes) from contents)) then 'ABOVE'
               else
               	'BELOW'
              end as Remarks
            from contents 
            Group by content_id 
            HAVING imdb_score_votes < (select AVG(imdb_Score_votes) from contents)
            ORDER BY content_id ASC ;''')

api_handle.commit_api()

row = cur.fetchone()

while row is not None:
	print(row)
	row = cur.fetchone()

print('Total Rows: ',cur.rowcount)

api_handle.close_api()
