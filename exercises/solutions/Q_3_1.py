
from postgresql_api import *


api_handle = postgresql_api()
cur = api_handle.connect_db()

cur.execute('''SELECT * from contents where content_rating = 
				(select content_rating_id from content_ratings 
					where name ILIKE 'TV-MA');''')

api_handle.commit_api()

row = cur.fetchone()

while row is not None:
	print(row)
	row = cur.fetchone()

print('Total Rows: ',cur.rowcount)

api_handle.close_api()
