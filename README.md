'''Step ONE:SETUP'''
# Set up a virtual environment for your final Project. Libraries should include:
    # - BeautifulSoup - for parsing the internet
    # - requests - for requesting a specific page
    # - psycopg2 - for using SQL
# - Make sure you also ad a requirements.txt file!

'''STEP TWO: CACHING'''
# - Set up your caching system. Borrow code from Project 3 which did something similar for data scraped from a website
# - Remember to cite your caching function (i.e. Project 3)
#
'''STEP THREE: SCRAPING'''
# - Use beautiful soup to find the blog posts you want on 826 website:
    # - main site: https://www.826michigan.org/
    # - blog page: https://www.826michigan.org/blog/
    # - Click "See More" at bottom of page to collect more postings...
#
'''STEP FOUR: CLASSES'''
# - Set up a Blog class for the data returned from scraping. Data extracted in the constructor should include:
    # - Date posted
    # - Blog URL
    # - Blog Title
    # - Blog Description
# - Use a method in your class to format the date from:
# "27" "Monday" "November 2017" to 11/27/2017 using datetime library
# - Also include a __repr___ method (to make a unique ID for each blog post)
# - Also include a __contains__ method (borrow from contains method in Project 3)
# - Create another method (that uses the contains method) to categorize blogs into the following groups: Use if/else statments to make this a thing.
    # - If title contains "FEATURED" --> "Featured Writing"
    # - If title contains "826" --> "About the Org"
    # (Once you get a look at the titles fully, think about other categories that might crop up)

'''STEP FIVE: DATABASE'''
# - Use terminal commands to set up a database for this project. Use TeamSQL to visualize
# - Borrow code from Project 6 to setup a database. Make two tables:
#     - One for blog entries (Columns = ID, Title, URL, Description, Date, Category)
#     - another for blog categories (Columns = ID, Category) *Make Sure you have at least 4 categories*
# - Adapt Project 6 code to input data directly from your Class definition into the DATABASE (?)

'''STEP SIX: UNITTESTS'''
# - Write unittests for your code. Borrow from Project 6 and Project 3 unittests
# - Save these in a separate file named "SI507F17_finalproject_tests.py"

'''STEP SEVEN: VISUALIZATION'''
(Get some more help from Jackie for this part...)
# - Create an HTML file with the kind of template you want to portray in your final project (use code from Project 6.5 to do so). Would contain semantic information like:
# - How many featured student pieces are there in the blog?
# - Or use plotly to map out -
# - Most common Category
# -

'''STEP EIGHT: README'''
# - Use these instructions as the basis for your readme. Written in outline format, it tells us exactly what to do to understand and run your code:
#
# - Logistics of running code...
#       - what precisely to type at a command prompt to run the code,
#       - what name of database they must create for the code to work,
#       - that they should pip install everything to `requirements.txt`,
#       - what version of Python the project expects (e.g. Python 3),
#       - if they need to fill in their own key and secret in a sample `secret_data.py` file in order to run the code, and what URLs they should go to to find the right key and secret…any information they might need)
#
# - And also...
#     - Basically what happens when the code runs (e.g. what classes are defined or what a couple major functions’ input / output will be, what database tables are created and used…)
#     - What the user should expect after the code runs (what should they see, what do any numbers they see represent, what will get created at the end — a file? a chart? — and how they can view it, etc)
#
# - Finally...
#     - Links to any resources used (e.g. client libraries, API documentation) and citations of any code borrowed from elsewhere
#     - Also include in the readme a list of everyone with whom you worked on any of the project or talked to about it in depth. Doing that is OK: sourcing help from others is great! But no two projects should be alike — this should be your own work.
