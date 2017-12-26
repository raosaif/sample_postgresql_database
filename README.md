# sample_postgresql_database
Welcome! This PostgreSQL repository will help you to understand PostgreSQL quickly with examples and sample database. 
in this repository's database (imdb), you will be introduced to a PostgreSQL sample database that you can use for learning and practice PostgreSQL.

We will use the imdb database for demonstrating the features of PostgreSQL. This database is built up personally for learning purpose. The main purpose of this task was to get familiar with PostgreSQL and python adaptor of PostgreSQL (psycopg2). 

### Relationship Layout

![](https://github.com/raosaif/sample_postgresql_database/blob/master/images/relationship_layout.jpg)

### Tabular Layout

![](https://github.com/raosaif/sample_postgresql_database/blob/master/images/tabular_layout.jpg)

For detail overview of the tables, please navigate to 'Schema' folder and click the index.html file. 

### There are 11 tables in the imdb database:

1- actors – stores actors data including name and actor_id.

2- contents – stores films/tv_shows data such as title, release_year,content_rating,user_voting, etc.

3- content_actors – stores the relationships between contents and actors.

4- content_types – stores content types.

5- content_ratings - stores content ratings. https://en.wikipedia.org/wiki/TV_parental_guidelines_(US)

6- content_directors - stores the relationships between contens and directors.

7- content_genres - stores the relationships between contents and genres.

8- directors - stores the information about directors including name and director_id.

9- genres - stores the information about imdb genres. http://www.imdb.com/feature/genre/?ref_=tt_ov_inf

10- episode_list - stores the inforamtion about episodes for each season of the tv shows.

11- languages - stores the information about the languages. (independent table)

# 1- Installation

There are three ways of restoring the database

##1- from imdb
Navigate to from_imdb directory and run the below command. You will need ![beautiful soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and ![urrlib](https://urllib3.readthedocs.io/en/latest/) for this operation. 
```
python3 imdb_upload_data
```
