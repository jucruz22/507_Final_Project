import psycopg2
import psycopg2.extras
from bs4 import BeautifulSoup
from datetime import datetime
from creds import *
import unittest
import requests
import json

"""CONSTANTS"""
CACHE_FNAME = 'cache_file_826michigan.json'
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

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






"""EXPERIMENTATION"""
# michigan826_html = CACHE_DICTION['https://www.826michigan.org/blog/']['html']
# michigan826_soup = BeautifulSoup(michigan826_html,'html.parser')
# # print(michigan826_soup)
# # print (michigan826_soup)
# blog_list = michigan826_soup.find("div",{"id":"content"}).find_all("div",{"class":"blog_cont"})
# # print(len(blog_list)) # Success!
# one_blog = blog_list[0]
# date_of_month = one_blog.find("div",{"class":"blog_date sprites date_textbg"}).text
# day_of_week = one_blog.find("div",{"class":"blog_cdaymonth"}).find("span").text
# month_year = one_blog.find("div",{"class":"blog_cdaymonth"}).text
# url = one_blog.find("div",{"class":"blog_title2"}).find('a')['href']
# title = one_blog.find("div",{"class":"blog_title2"}).find('a').text
# description = one_blog.find("div",{"class":"blog_text"}).find('p').text
# month_year = month_year.split('y')[1]
# day_month_year = str(date_of_month) + " " + month_year
# dt_obj = datetime.strptime(day_month_year, '%d %B %Y')
# converted_date = dt_obj.strftime('%Y-%m-%d')

# print(converted_date)
# print(day_month_year)
# print(month_year)
# print(date_of_month)
# print(day_of_week)
# print (month_year) #  MondayNovember 2017
# print(url)
# print(title)
# print (description)
