from os import path
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
from creds import *
import psycopg2
import psycopg2.extras
import unittest
import requests
import json

"""CONSTANTS"""
CACHE_FNAME = 'cache_file_826michigan.json'
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

# For visualization later...
stop_words = []
fstop = open('stop_words.txt', 'r')
for word in fstop.readlines():
    # stop_words.append(unicode(word.strip()))
    stop_words.append(word.strip())
fstop.close()

"""CACHING"""
# If CACHE exists, convert to dictionary format using json.loads()
try:
    with open(CACHE_FNAME, 'r') as cache_file:
        cache_json = cache_file.read()
        CACHE_DICTION = json.loads(cache_json)
except:
    CACHE_DICTION = {}

def get_and_set_in_cache(url):
    # Create unique identifer for all new requests and add to your cache dictionary.
    # Simultaneously add to cache but function should return the HTML of what you wanna parse

    # Try and see if your url is in the cache dictionary already
    if url in CACHE_DICTION:
        print ('Loading from cache: {0}'.format(url))
        html = CACHE_DICTION[url]['html']

    # If not, make a request on that URl and set it in cache
    else:
        print('Fetching a fresh copy: {0}'.format(url))
        response = requests.get(url)
        response.encoding = 'utf-8'
        html = response.text

        CACHE_DICTION[url] = {
            'timestamp': datetime.now().strftime(DATETIME_FORMAT),
            'html': html
             # date today
        }

        with open(CACHE_FNAME, 'w') as cache_file:
            cache_json = json.dumps(CACHE_DICTION)
            cache_file.write(cache_json)

    return html

"""OTHER FUNCTIONS"""
def get_blog_list(html):
    soup = BeautifulSoup(html,'html.parser')
    blog_list = soup.find("div",{"id":"content"}).find_all("div",{"class":"blog_cont"})
    return blog_list

# test1 = get_and_set_in_cache('https://www.826michigan.org/')
# test2 = get_and_set_in_cache('https://www.826michigan.org/blog/')
# print(CACHE_DICTION['https://www.826michigan.org/blog/'])
"""CLASS CREATION"""
class Blog(object):
    def __init__(self,blog_soup):
        try:
            self.date_of_month = blog_soup.find("div",{"class":"blog_date sprites date_textbg"}).text
            self.day_of_week = blog_soup.find("div",{"class":"blog_cdaymonth"}).find("span").text
            self.month_year = blog_soup.find("div",{"class":"blog_cdaymonth"}).text
            self.url = blog_soup.find("div",{"class":"blog_title2"}).find('a')['href']
            self.title = blog_soup.find("div",{"class":"blog_title2"}).find('a').text
            self.description = blog_soup.find("div",{"class":"blog_text"}).find('p').text
        except:
            self.date_of_month = None
            self.day_of_week = ""
            self.month_year = ""
            self.url = ""
            self.title = ""
            self.description = ""

    def convert_date(self):
        try:
            month_year = self.month_year.split('y')[1]
            day_month_year = str(self.date_of_month) + " " + month_year
            dt_obj = datetime.strptime(day_month_year, '%d %B %Y') # sets these variables in place
            return dt_obj.strftime('%Y-%m-%d') # '2017-11-27'
        except:
            return None


    def blog_category(self):
        if 'Featured' in self.title:
            category = 'Featured Writing'
        elif 'Foundation' in self.title:
            category = 'Featured Foundation'
        elif 'Supporter of the Month' in self.title:
            category = 'Featured Supporter'
        else:
            category = 'Other'
        return category

    def unique_words(self):
        punctuation = '()!@#$%^&*?~.,…'
        lower_case = self.description.lower()
        temp = lower_case.split() # split text string by its spaces
        word_list = []

        # getting rid of punctuation in all the words
        for w in temp:
            for ch in w:
                if ch in punctuation:
                    removed = w.replace(ch, "")
                    w = removed
            word_list.append(w)

        # getting rid of stop words
        unique_words = []
        for w in word_list:
            if w not in stop_words:
                unique_words.append(w)

        return unique_words

    def __repr__(self):
        month_year = self.month_year.split('y')[1]
        day_month_year = str(self.date_of_month) + " " + month_year
        return "'{}' published on {}".format(self.title,day_month_year)

    def __contains__(self,word):
        if word in self.title:
            return True
        else:
            return False

"""PARSING"""
# Creating html list from most recent 3 pages of blog content on 826michigan website
michigan826_html_1 = get_and_set_in_cache('https://www.826michigan.org/blog/')
blog_list_1 = get_blog_list(michigan826_html_1)
michigan826_html_2 = get_and_set_in_cache('https://www.826michigan.org/blog/page/2/')
blog_list_2 = get_blog_list(michigan826_html_2)
michigan826_html_3 = get_and_set_in_cache('https://www.826michigan.org/blog/page/3/')
blog_list_3 = get_blog_list(michigan826_html_3)
blog_list = blog_list_1 + blog_list_2 + blog_list_3
# print(len(blog_list))
blog_objs = [Blog(b) for b in blog_list]
# for b in blog_objs:
#     print(b.blog_category())

"""DATABASE"""
def execute_and_print(query, numer_of_results=1):
    # this function does what lines 27-32 did just now so that you don't have to repeat it every time
    cur.execute(query) # executes a query using the .execute function in psycopg2
    results = cur.fetchall() # AFTER query is made, still need to ascribe a variable to the results
    for r in results[:numer_of_results]: # cut a list only to the 1st index
        print(r) # prints only the first result even tho fetchall is used
    print('--> Result Rows:', len(results)) # prints the length of results using fetchal i.e. the number of columns returned, depending on the query
    print()

def get_connection_and_cursor():
    try:
        if db_password != "":
            db_connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
            print("Success connecting to database")
        else:
            db_connection = psycopg2.connect("dbname='{0}' user='{1}'".format(db_name, db_user))
    except:
        print("Unable to connect to the database. Check server and credentials.")
        sys.exit(1) # Stop running program if there's no db connection.

    db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, db_cursor

conn, cur = get_connection_and_cursor()

# Creating tables
cur.execute('DROP TABLE IF EXISTS "Blogs"')
cur.execute('DROP TABLE IF EXISTS "Categories"')

# Make Categories table first, so that can refer to it in Blogs (Foreign Key)
cur.execute(""" CREATE TABLE IF NOT EXISTS "Categories"(
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(40) UNIQUE
    )""")

# Now make Blogs table, where Category_ID references ID in Categories table (PRIMARY KEY)
cur.execute(""" CREATE TABLE IF NOT EXISTS "Blogs"(
    ID SERIAL PRIMARY KEY,
    Title VARCHAR(128) UNIQUE,
    Date_Published DATE,
    URL TEXT,
    Description TEXT,
    Cat_ID INTEGER REFERENCES "Categories"(ID)
    )""")

# Commit these changes
conn.commit()

# Create Categories table
cur.execute("""INSERT INTO "Categories" (Name) VALUES('Featured Writing')""")
cur.execute(""" INSERT INTO "Categories" (Name) VALUES('Featured Foundation') """)
cur.execute(""" INSERT INTO "Categories" (Name) VALUES('Featured Supporter') """)
cur.execute(""" INSERT INTO "Categories" (Name) VALUES('Other') """)

# Commit these changes
conn.commit()

# Create Blogs table
# iterate through blog instance blog_list
# add each blog entry to the DATABASE
def get_category_id(cat_name):
    cur.execute(""" SELECT ID FROM "Categories" WHERE Name=%s """, (cat_name, ))
    results = cur.fetchall()
    # print (results) # [{'id': 2}]
    cat_id = results[0]['id']
    return cat_id

for b in blog_objs:
    cur.execute(""" INSERT INTO
        "Blogs" (Title,Date_Published,URL,Description,Cat_ID)
        VALUES(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING """,
        (b.title,b.convert_date(),b.url,b.description,get_category_id(b.blog_category()))
        )
conn.commit()
print ("Successfully transfered blog class data to Database") # YASSSS :)


"""VISUALIZATION - WORD CLOUD"""
# Making a word cloud of most common words using blog description text
# Code adapted from: https://github.com/amueller/word_cloud/blob/master/examples/simple.py
massive_str = ""
for b in blog_objs:
    massive_str = massive_str + b.description

# print(massive_str)

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, '826michigan_words.txt')).read()
# print(text)

# Generate a word cloud image
mask = np.array(Image.open(path.join(d,'gear.png')))
wordcloud = WordCloud(background_color="white",max_words=len(massive_str),mask=mask).generate(massive_str)
wordcloud.to_file(path.join(d,'826_wordcloud.png'))
print('Successfully created wordcloud PNG file')

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

"""VISUALIZATION - HTML"""
def top_five_words(blog_list,blog_cat=None):
    most_common = {}

    # Selecting blogs by category
    for b in blog_list:
        if b.blog_category() == blog_cat:
            for word in b.unique_words():
                most_common[word] = most_common.get(word, 0) + 1
        elif blog_cat==None:
            for word in b.unique_words():
                most_common[word] = most_common.get(word, 0) + 1

    # Sorting
    sort_most_common = sorted(most_common, key=lambda w: most_common[w], reverse=True)
    top_five = sort_most_common[:5]

    return blog_cat.upper(), top_five

# print (top_five_words(blog_objs,'Featured Writing'))

# Make most common words from 826 blogs into its own html file
f = open('826michigan.html','w')
f.write("""
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="utf-8">
	<title>826 Michigan</title>
	<!-- <link rel="stylesheet" type="text/css" href="css/style.css"> -->
	<style>
		body {
			background-color: #e37600;
		}
	</style>
</head>

<body>
	<p>These are the top 5 words referenced throught 826michigan's online blog:</p>

	<h1>Entire Blog</h1>

		<ol>
			<li>detroit</li>
			<li>826michigan</li>
			<li>school</li>
			<li>year</li>
			<li>age</li>
		</ol>

	<p>These are the top 5 words per category:</p>

	<h1>Featured Writing</h1>

		<ol>
			<li>age</li>
			<li>friend</li>
			<li>day</li>
			<li>like</li>
			<li>school</li>
		</ol>

	<h1>Featured Foundations</h1>

		<ol>
			<li>foundation</li>
			<li>start</li>
			<li>school</li>
			<li>year</li>
			<li>fall</li>
		</ol>

	<h1>Featured Supporter</h1>
		<ol>
			<li>writing</li>
			<li>community</li>
			<li>pizza</li>
			<li>domino's</li>
			<li>family</li>
		</ol>

	<h1>Other</h1>

		<ol>
			<li>826michigan</li>
			<li>detroit</li>
			<li>month</li>
			<li>love</li>
			<li>students</li>
		</ol>

</body>
""")
f.close()
print ('Successfully created 826 Michigan html file')
