
from postgresql_api import *


api_handle = postgresql_api()
cur = api_handle.connect_db()

cur.execute('''SELECT * from contents 
INNER JOIN content_ratings ON content_ratings.content_Rating_id = contents.content_rating
where content_ratings.name ILIKE 'TV-MA';''')

api_handle.commit_api()

row = cur.fetchone()

while row is not None:
	print(row)
	row = cur.fetchone()

print('Total Rows: ',cur.rowcount)

api_handle.close_api()
