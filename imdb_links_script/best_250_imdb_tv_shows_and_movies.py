from bs4 import BeautifulSoup
import urllib.request
import re
import json
import sys
import urllib3

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


def main(argv):
	website_url = []

	website_url.append('http://www.imdb.com/chart/toptv?ref_=tt_awd') #TV-Shows
	website_url.append('http://www.imdb.com/chart/top?ref_=tt_awd')   #Movies
	imdb_url = 'http://www.imdb.com'

	main_list = []
	main_dict = {}

	for url in range(len(website_url)):
		print(website_url[url])

		soup = BeautifulSoup(get_url_response(website_url[url]),'lxml') # to get the html source of the page
		tBody = soup.find('tbody',class_='lister-list').find_all('td',class_='titleColumn')

		for link in range(len(tBody)):
			sub_dict = {}
			sub_dict['id'] = link
			sub_dict['title'] = tBody[link].find('a').string
			sub_dict['imdb_url'] = imdb_url +tBody[link].find('a')['href'] 
			sub_dict['status'] = 'NOT_YET_UPLOADED'
			main_list.append(sub_dict)
		
		main_dict['total_links'] = len(main_list)
		main_dict['links'] = main_list
	
	with open('Links' +'.json', 'w') as fp:
		json.dump(main_dict, fp,indent=4)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
