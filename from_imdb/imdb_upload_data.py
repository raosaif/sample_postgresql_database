#!/usr/bin/python3   

from bs4 import BeautifulSoup
import urllib.request
import re
import json
import requests
import sys
import urllib3
from postgresql_api import *
from imdb_ratings import *


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_url_response(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	html = ''
	try:
		req = urllib.request.Request(url, None, hdr)
		with urllib.request.urlopen(req) as response:
			html = response.read()
		return html

	except:
	    print('error')


def imdb_upload_data(api_handle,imdb_url,website_url):

	season_dict = {} # Main Dictonary
	content_type = ''
	content_data = {} # for database

	soup = BeautifulSoup(get_url_response(website_url),'lxml') # to get the html source of the page


	release_info = soup.find('a',title=re.compile('release dates'))
	for info in release_info.stripped_strings:
		season_dict['release_dates'] = info

	print("Release Dates: ",season_dict['release_dates'])
	isDocumentary = False

	#Genre
	genres = soup.find_all('span',itemprop='genre')
	genres_list = []
	for genre in range(len(genres)):
		#print(genres[genre].string)
		genres_list.append(genres[genre].string)
		if('Documentary' in genres[genre].string):
			isDocumentary = True

	season_dict['genre'] = genres_list
	content_data['genre'] = genres_list

	if('TV' not in info):
		content_type = 'M'
		content_data['total_seasons'] = 1
		content_data['total_episodes'] = 1
	else:
		if(isDocumentary):
			content_type = 'D'
			season_dict['release_dates'] = season_dict['release_dates'].replace('TV Mini-Series','')
			season_dict['release_dates'] = season_dict['release_dates'].strip(' ()')
			content_data['total_seasons'] = 1
			content_data['total_episodes'] = 1
		else:
			content_type = 'T'
			season_dict['release_dates'] = season_dict['release_dates'].replace('TV Series','')
			season_dict['release_dates'] = season_dict['release_dates'].strip(' ()')

	#print(season_dict['release_dates'])
	#print(content_type)
	content_data['release_dates'] = season_dict['release_dates']

	duration = None
	duration = soup.find('time',itemprop='duration')
	if(duration != None):
		for cur in duration.stripped_strings:
			season_dict['duration'] = cur 

		print(season_dict['duration'])
		content_data['play_time'] = season_dict['duration']
	else:
		content_data['play_time'] = 'NA'

	content_data['imdb_link'] = website_url
	#Title
	title = soup.find('h1',itemprop='name')
	if(content_type == 'T'):
		season_dict['title'] = " ".join(title.string.split())
	else:
		season_dict['title'] = 	" ".join(title.contents[0].split())

	original_title = None
	original_title_string = ''
	original_title != soup.find('div',class_='originalTitle')
	if(original_title != None):
		for string in soup.find('div',class_='originalTitle').strings:
			original_title_string = original_title_string + string
		
		season_dict['title'] = season_dict['title'] +'-' +  original_title_string

	content_data['title'] = season_dict['title']
	print('Title: ',content_data['title'])

	#Rating
	season_rating = soup.find('span',itemprop='ratingValue')
	#print(season_rating.string)
	season_dict['season_ratings'] = season_rating.string
	content_data['overall_rating'] = season_rating.string

	#Rating Count
	season_user_ratings = soup.find('span',itemprop='ratingCount')
	#print(season_user_ratings.string)
	season_dict['imdb_score_votes'] = season_user_ratings.string
	content_data['imdb_score_votes'] = int(season_user_ratings.string.replace(',',''))
	#print('Votes: ', content_data['imdb_score_votes'])

		#Ratings Json
	rating_link = soup.find('div',class_='imdbRating').find('a',href=re.compile("ratings"))['href']
	print('Rating Link: ', rating_link)
	rating_json = making_ratings_json(BeautifulSoup(get_url_response(imdb_url+rating_link),'lxml'),content_data['imdb_score_votes'],imdb_url+rating_link)
	content_data['rating_details'] = rating_json


	#Content Rating
	content_rating = None
	content_rating = soup.find('meta',itemprop='contentRating')
	# #print(content_rating['content'])
	if(content_rating != None):
		content_data['content_rating'] = content_rating['content']
	else:
		content_data['content_rating'] = 'NA'

	season_dict['content_rating'] = content_data['content_rating']

	#Creators
	season_creators = []
	creators=''
	if(content_type == 'T'):
		creators = soup.find_all('span',itemprop='creator')
	elif (content_type == 'M'):
		creators = soup.find_all('span',itemprop='director')
	elif (content_type == 'D'):
		creators = soup.find_all('span',itemprop='actors')

	for creator in range(len(creators)):
		season_creators.append(creators[creator].find('span',itemprop='name').string)
		#print(creators[creator].find('span',itemprop='name'))

	season_dict['creators'] = season_creators
	content_data['directors'] = season_dict['creators']

	#print(season_dict['creators'])

	#Cast
	cast_characters = []
	all_cast = soup.find('table',class_='cast_list')
	cast_name = all_cast.find_all('span',itemprop='name')
	character_name = all_cast.find_all('td',class_='character')
	for names in range(len(cast_name)):
		cast_characters.append(cast_name[names].string)
		#print(cast_name[names].string)
	season_dict['cast'] = cast_characters
	content_data['cast'] = season_dict['cast']
	api_handle.insert_directors(season_creators)
	api_handle.insert_actors(cast_characters)
	api_handle.commit_api();

	languages_list = []
	languages = soup.find_all('a',href=re.compile("primary_language="))
	for lan in range(len(languages)):
		print('Languages: ', languages[lan].string)
		languages_list.append(languages[lan].string)
	
	api_handle.insert_languages(languages_list)
	api_handle.commit_api()

	content_data['languages'] = languages_list
	season_dict['languages'] = languages_list
	#Season Description
	season_description = soup.find('div', itemprop='description')
	for description in season_description.stripped_strings:
		season_dict['season description'] = description
		content_data['description'] = description
		#print(description)

	###################inserting###############
	if(content_type == 'M' or content_type == 'D'):
		ret = api_handle.insert_content_data(content_data,content_type)
		if(ret):
			pass
			api_handle.commit_api()

	if(content_type == 'T'):

		#Episode Guide
		episode_guide = soup.find_all('span',class_='bp_sub_heading')
		for total_epi in range(len(episode_guide)):
			#print('List: ',episode_guide[total_epi].string)
			if('episode' in episode_guide[total_epi].string):
				season_dict['total episodes'] = episode_guide[total_epi].string
				#print(episode_guide[total_epi].string.split()[0])
				content_data['total_episodes'] = int(episode_guide[total_epi].string.split()[0])
			#print(episode_guide.string)


		#Season Episode
		season_episode = None
		season_episode = soup.find_all('a',href=re.compile("season="))
		if(season_episode != None):
			season_dict['total_seasons'] = season_episode[0].string
			#print('total seasons: ',season_episode[0].string)
		else:
			season_dict['total_seasons'] = 0
		

		season_year = soup.find_all('a',href=re.compile("ref_=tt_eps_yr_"))

		print('Latest Year: ',season_year[0].string)
		latest_year = season_year[0].string

		if(RepresentsInt(season_episode[0].string)):
			if(int(latest_year) > 2017):
				season_to_search = int(season_episode[0].string)-(int(latest_year)-2017)
			else:
				season_to_search = int(season_episode[0].string)

			print('Season to Search: ', season_to_search)
		else:
			season_to_search = 0



		season_link = season_episode[0]['href'] # /title/tt0108778/episodes?season=10&ref_=tt_eps_sn_10
		content_data['total_seasons'] = season_to_search


		ret = api_handle.insert_content_data(content_data,content_type)
		if(ret):
			pass
			api_handle.commit_api()

		db_episodes = {}

		per_season_list = []
		count_total_episodes = 0
		count_total_seasons = 0

		for each_season in range(season_to_search):
		#for each_season in range(1):
			db_episodes['season_num'] = each_season
			per_season_dict = {}
			per_episode_list = []
			season_url = imdb_url + season_link[:season_link.find('=')+1] + str(each_season+1) + '&ref_=tt_eps_sn_' + str(each_season+1)
			print('='*60)
			print(content_data['title'], '-',each_season + 1 , season_url)
			print('='*60)

			each_season_soup = BeautifulSoup(get_url_response(season_url),'lxml')

			episodes_link = each_season_soup.find_all('div',itemprop='episodes')
			#print(len(episodes_link))
			#print(episodes_link[0])
			for every_episode in range(len(episodes_link)):
				count_total_episodes = count_total_episodes + 1
				per_episode_dict = {}
				db_episodes['title'] = " ".join(title.string.split())
				db_episodes['release_dates'] = content_data['release_dates']
				db_episodes['episode_num'] = every_episode
				db_episodes['episode_name'] = episodes_link[every_episode].find('a',itemprop='name')['title']
				#print(db_episodes['episode_name'])

				#each_episode_soup= BeautifulSoup(episodes_link[every_episode],'lxml')
				episode_release_date = None
				episode_release_date = episodes_link[every_episode].find('div',class_='airdate')
				#print('Here: ',episode_release_date)

				if(episode_release_date != None ):
					for airDate in episode_release_date.stripped_strings:
						#print('Air Date: ',airDate)
						if(len(airDate) > 2):
							per_episode_dict['release_date'] = airDate
						else:
							per_episode_dict['release_date'] = 'NA'
					else:
						per_episode_dict['release_date'] ='NA'
				else:
					per_episode_dict['release_date'] = 'NA'

				db_episodes['release_date'] = per_episode_dict['release_date']

				db_episodes['episode_imdb_link'] = imdb_url + episodes_link[every_episode].find('a',itemprop='name')['href']
				per_episode_dict['episode_imdb_link'] = db_episodes['episode_imdb_link']
				#print(db_episodes['episode_imdb_link'])


				#print(episodes_link[every_episode].find('span',class_=re.compile('ipl-rating-star__rating')).string)
				if(episodes_link[every_episode].find('span',class_=re.compile('ipl-rating-star__total-votes')) != None):
					per_episode_dict['rating'] = episodes_link[every_episode].find('span',class_=re.compile('ipl-rating-star__rating')).string
					db_episodes['episode_rating'] = float(episodes_link[every_episode].find('span',class_=re.compile('ipl-rating-star__rating')).string)

					#print(episodes_link[every_episode].find('span',class_=re.compile('ipl-rating-star__total-votes')).string)
					per_episode_dict['episode_score_votes'] = episodes_link[every_episode].find('span',class_=re.compile('ipl-rating-star__total-votes')).string
					db_episodes['episode_score_votes'] = int(episodes_link[every_episode].find('span',class_=re.compile('ipl-rating-star__total-votes')).string.strip('()').replace(',',''))

					for every_description in episodes_link[every_episode].find('div',class_='item_description').stripped_strings:
						#print(every_description)
						per_episode_dict['episode_description'] = every_description
						db_episodes['episode_description'] = every_description


					#print (json.dumps(per_episode_dict,indent=4))
					if(api_handle.is_episode_not_exists(db_episodes)):
						ret = api_handle.insert_episodes(db_episodes)
						if(ret):
							api_handle.commit_api()
					else:
						print('Episode Information Already exisits so skipping the webURL')

					per_episode_list.append(per_episode_dict)
					#print('Length: ',len(per_episode_list))
				
			per_season_dict['season-'+str(each_season+1)] = per_episode_list
			per_season_list.append(per_season_dict)


		season_dict['Seasons'] = per_season_list
		if(count_total_episodes != content_data['total_episodes']):
			print('Updating Total Episodes: ', count_total_episodes ,' and ', content_data['total_episodes'])
			content_data['total_episodes'] = count_total_episodes
			api_handle.updating_total_episodes(content_data)
			api_handle.commit_api()
	


	#with open(content_data['title'] +'.json', 'w') as fp:
		#json.dump(season_dict, fp,indent=4)
	

	#print (json.dumps(season_dict,indent=4))
	return "SUCCESS"

def main(argv):

	api_handle = postgresql_api()
	api_handle.connect_db(dbname='imdb',user='username',host='localhost',password='password')

	with open('../imdb_links_script/Links.json', 'r') as f:
		data = json.load(f)

	print(len(data['links']))

	imdb_url = 'http://www.imdb.com'

	for eachLink in range(len(data['links'])):
		if(data['links'][eachLink]['status'] != 'UPLOADED'):
			ret = imdb_upload_data(api_handle,imdb_url,data['links'][eachLink]['imdb_url'])
			if ('SUCCESS' in ret):
				data['links'].pop(eachLink)

				with open('Links' +'.json', 'w') as fp:
					json.dump(data, fp,indent=4)
					
			print('***********Uploaded***********')

	api_handle.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))