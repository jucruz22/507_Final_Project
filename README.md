# Project Overview
This script involves a little bit of web-scraping, data-parsing, database creation, and data visualization. The whole package! More specifically, I've scraped from the website of one of my favorite organizations; **826 Michigan** is a reading and writing center in Ann Arbor, pleasantly disguised a pirate supply shop (website: https://www.826michigan.org/)  

# Getting Started
- To begin, you'll want to pip install all libraries included in the **requirements.txt** file into your own virtual environment. This code runs using Python 3.6.
- You will also want a separate **creds.py** file (not included here) that contains the following (please note db_name should not be changed):

```
db_name = 'jucruz-final-project-db'
db_user = 'your_terminal_username'
db_password = 'your_computer_password'
```
- Finally, you will need access to the PostgreSQL database server and (optionally) a database viewer (i.e. TeamSQL). Instructions to download the former can be found here: https://paper.dropbox.com/doc/Postgres-Database-setup-N4y2qlUr5BeP1X42Z5suc

# What to Expect
Once you're set up in your virtual environment, to run the code, type in the following command:
```
python SI507F17_finalproject.py
```
If it works successfully, you should see the following:
```
Fetching a fresh copy: https://www.826michigan.org/blog
Fetching a fresh copy: https://www.826michigan.org/blog/page/2/
Fetching a fresh copy: https://www.826michigan.org/blog/page/3/
Success connecting to database
Successfully transferred blog class data to Database
```
Essentially what's happening in the background is as follows:
- HTML data is scraped using BeautifulSoup and cached in a file called **cache_file_826michigan.json**
- That data is then parsed through to acquire a list of blog HTML objects
- A class Blog retrieves date, url, title, and description information for each of these objects
- This information is then input into a database called 'jucruz-final-project-db' in the form of two tables:
  - Blogs
  - Categories (They are linked by the Categories Primary Key)
-


# Libraries Used
- **psycopg2**: PostgreSQL adapter for the Python programming language
- **BeautifulSoup**: Used to extract data from HTML during web scraping
- **datetime**: For manipulating dates and times in both simple and complex ways
- **unittest**: Supports test automation
* Other built-in libraries include json and requests

# Acknowledgments
- Many thanks to https://www.postgresql.org/ for their thorough documentation on how to interact with a database via Python
- Additional gratitude for our class documentation, particularly from [Project 3](https://github.com/jucruz22/SI507-Project3) and [6](https://github.com/jucruz22/SI507-Project6)
- Hats off to 826 Michigan for the work they do locally and for letting me peruse their site for educational purposes
- Another dose of thanks to our "Code Champs" group within our SI 507 class, including Kenji Kaneko, Stefan Deuchler, and Vibhuti Kanitkar
- And finally, rounds of applause to my noble teachers, [Jackie Cohen](https://github.com/aerenchyma) and [Anand Doshi](https://github.com/anandpdoshi) for their patient instruction, playful trouble-shooting, and empathetic skills throughout the process of my learning how to program in Python :)
