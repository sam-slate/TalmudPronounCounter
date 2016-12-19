import urllib2 # to make api calls to sefaria 
import json #to turn string from sefaria into json
from collections import Counter #to get counter functionality 
import collections #to sort the dictionary
import csv #to make the excel spreadsheet

#Makes a list of words that would be considered to be he series pronouns
#The strings with <i></i> are included to account for the API passing in HTML 
he_series_pronouns = ["he", "him", "his", "He", "Him", "His", 
					  "he.", "him.", "his.", "he,", "him,", "his,",
					  "he:", "him:", "his:", "he;", "him;", "his;",
					  "he!", "him!", "his!", "he?", "him?", "his?",
					  "<i></i>he", "<i></i>him", "<i></i>his", "<i></i>He", "<i></i>Him", "<i></i>His", 
					  "<i></i>he.", "<i></i>him.", "<i></i>his.", "<i></i>he,", "<i></i>him,", "<i></i>his,",
					  "<i></i>he:", "<i></i>him:", "<i></i>his:", "<i></i>he;", "<i></i>him;", "<i></i>his;",
					  "<i></i>he!", "<i></i>him!", "<i></i>his!", "<i></i>he?", "<i></i>him?", "<i></i>his?",
					  "he<i></i>", "him<i></i>", "his<i></i>", "He<i></i>", "Him<i></i>", "His<i></i>", 
					  "he.<i></i>", "him.<i></i>", "his.<i></i>", "he,<i></i>", "him,<i></i>", "his,<i></i>",
					  "he:<i></i>", "him:<i></i>", "his:<i></i>", "he;<i></i>", "him;<i></i>", "his;<i></i>",
					  "he!<i></i>", "him!<i></i>", "his!<i></i>", "he?<i></i>", "him?<i></i>", "his?<i></i>"]

#Makes a list of words that would be considered to be she series pronouns
#The strings with <i></i> are included to account for the API passing in HTML
she_series_pronouns = ["she", "her", "hers", "She", "Her", "Hers", 
                       "she.", "her.", "hers.", "she,", "her,", "hers,",
                       "she:", "her:", "hers:", "she;", "her;", "hers;",
                       "she!", "her!", "hers!", "she?", "her?", "hers?",
                       "<i></i>she", "<i></i>her", "<i></i>hers", "<i></i>She", "<i></i>Her", "<i></i>Hers", 
                       "<i></i>she.", "<i></i>her.", "<i></i>hers.", "<i></i>she,", "<i></i>her,", "<i></i>hers,",
                       "<i></i>she:", "<i></i>her:", "<i></i>hers:", "<i></i>she;", "<i></i>her;", "<i></i>hers;",
                       "<i></i>she!", "<i></i>her!", "<i></i>hers!", "<i></i>she?", "<i></i>her?", "<i></i>hers?",
                       "she<i></i>", "her<i></i>", "hers<i></i>", "She<i></i>", "Her<i></i>", "Hers<i></i>", 
                       "she.<i></i>", "her.<i></i>", "hers.<i></i>", "she,<i></i>", "her,<i></i>", "hers,<i></i>",
                       "she:<i></i>", "her:<i></i>", "hers:<i></i>", "she;<i></i>", "her;<i></i>", "hers;<i></i>",
                       "she!<i></i>", "her!<i></i>", "hers!<i></i>", "she?<i></i>", "her?<i></i>", "hers?<i></i>"]

#Creates a list of strings to add to the API url in order to get 
#each page in Berakhot. 
num_pages_berakhot = 63
list_of_pages = []

for x in range (2, (num_pages_berakhot + 1)):
	new_pagea = str(x) + 'a'
	new_pageb = str(x) + 'b'
	list_of_pages.append(new_pagea)
	list_of_pages.append(new_pageb)

list_of_pages.append("64a")

#Initializes an empty dictionary to store the pronouns and their frequency
dict_of_pronouns = {}

#Loops through each prepared string from above
for page in list_of_pages:

	#Prepares the URL by adding the current string 
	url = 'http://www.sefaria.org/api/texts/Berakhot.' + page
	
	#Makes the API call and creates a JSON file from the returned string
	content = urllib2.urlopen(url).read()
	contentjson = json.loads(content)

	#Gets the text object (a list of strings) from the JSON object 
	#and joins them to create one string
	text = contentjson["text"]
	textjoined = ' '.join(text)

	#Creates counts object which has the frequency of every word
	#in the textjoined string
	counts = Counter(textjoined.split())

	#Initializes the he series count and the she series count
	total_he_count = 0
	total_she_count = 0

	#Loops through the pronoun lists made earlier, looks up the frequency
	#of each pronoun in the counts object, and adds that frequency to the
	#respective count
	for pronoun in he_series_pronouns:
		total_he_count += counts[pronoun]

	for pronoun in she_series_pronouns:
		total_she_count += counts[pronoun]

	#Adds the total frequency of all he series and she series pronouns 
	#to the dictionary using as a key a string built out of the current 
	#page
	dict_entry_he = page + ' He Series'
	dict_entry_she = page + ' She Series'
	dict_of_pronouns[dict_entry_he] = total_he_count
	dict_of_pronouns[dict_entry_she] = total_she_count

#Creates an Excel spreadsheet off of the dictionary
with open('output.csv', 'wb') as output:
    writer = csv.writer(output)
    for key, value in dict_of_pronouns.iteritems():
        writer.writerow([key, value])


