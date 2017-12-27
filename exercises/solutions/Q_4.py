from postgresql_api import *


api_handle = postgresql_api()
cur = api_handle.connect_db()

cur.execute('''SELECT * from contents where 'Spanish' = ANY(contents.languages);''')

api_handle.commit_api()

row = cur.fetchone()

while row is not None:
	print(row)
	row = cur.fetchone()

print('Total Rows: ',cur.rowcount)

api_handle.close_api()
