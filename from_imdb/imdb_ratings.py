import json
import re

def making_ratings_json(rating_soup,total_votes,rating_page_link):
	rating_json = {}
	rating_json["total_votes"] = total_votes
	rating_json["rating_page_link"] = rating_page_link
	respective_votes = rating_soup.find_all('table')[0].find_all('td')
	count = 10
	cat_dict = {}

	for ind in range(len(respective_votes)):
		if(respective_votes[ind].find('div',class_='leftAligned') != None):
			#print(respective_votes[ind].find('div',class_='leftAligned').string)
			cat_dict[str(count)] = int(respective_votes[ind].find('div',class_='leftAligned').string.replace(',',''))
			count = count - 1

	#rating_json["votes_per_ratings"] = cat_dict

	cat_dict = {}
	cat_sub_dict = {}
	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[0].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[0].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes'"] = int([string for string in rating_soup.find('a',href=re.compile("demo=imdb_users")).stripped_strings][0].replace(',',''))
		cat_dict["all_votes"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[1].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[1].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=aged_under_18")).stripped_strings][0].replace(',',''))
		cat_dict["aged_under_18"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[2].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[2].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=aged_18_29")).stripped_strings][0].replace(',',''))
		cat_dict["aged_18_29"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[3].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[3].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=aged_30_44")).stripped_strings][0].replace(',',''))
		cat_dict["aged_30_44"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[4].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[4].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=aged_45_plus")).stripped_strings][0].replace(',',''))
		cat_dict["aged_over_45"] = cat_sub_dict	
	

	rating_json["all_genders"]= cat_dict #all

	cat_dict={}
	cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[5].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[5].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=males")).stripped_strings][0].replace(',',''))
		cat_dict["all_votes"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[6].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[6].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=males_aged_under_18")).stripped_strings][0].replace(',',''))
		cat_dict["aged_under_18"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[7].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[7].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=males_aged_18_29")).stripped_strings][0].replace(',',''))
		cat_dict["aged_18_29"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[8].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[8].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=males_aged_30_44")).stripped_strings][0].replace(',',''))
		cat_dict["aged_30_44"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[9].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[9].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=males_aged_45_plus")).stripped_strings][0].replace(',',''))
		cat_dict["aged_over_45"] = cat_sub_dict	


	rating_json["males"]= cat_dict #Males

	cat_dict={}
	cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[10].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[10].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=females")).stripped_strings][0].replace(',',''))
		cat_dict["all_votes"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[11].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[11].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=females_aged_under_18")).stripped_strings][0].replace(',',''))
		cat_dict["aged_under_18"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[12].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[12].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=females_aged_18_29")).stripped_strings][0].replace(',',''))
		cat_dict["aged_18_29"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[13].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[13].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=females_aged_30_44")).stripped_strings][0].replace(',',''))
		cat_dict["aged_30_44"] = cat_sub_dict
		cat_sub_dict = {}

	if('-' not in rating_soup.find_all('td',class_=re.compile('ratingTable'))[14].find('div',class_='bigcell').string):
		cat_sub_dict["rating"] = float(rating_soup.find_all('td',class_=re.compile('ratingTable'))[14].find('div',class_='bigcell').string)
		cat_sub_dict["total_votes"] = int([string for string in rating_soup.find('a',href=re.compile("demo=females_aged_45_plus")).stripped_strings][0].replace(',',''))
		cat_dict["aged_over_45"] = cat_sub_dict	
		rating_json["females"]=cat_dict

	#print (json.dumps(rating_json,indent=4))
	#print('TYPE: ',type(rating_json))
	return rating_json
