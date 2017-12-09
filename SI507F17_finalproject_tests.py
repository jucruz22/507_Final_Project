import unittest
from SI507F17_finalproject import *

class Caching(unittest.TestCase):
    def setUp(self):
        self.cache_file = open(CACHE_FNAME)

    def test_cache_exists(self):
        self.assertTrue(self.cache_file.read())

    def test_cache_diction(self):
        self.assertTrue(type(CACHE_DICTION),dict)

    def tearDown(self):
        self.cache_file.close()

class BlogClass(unittest.TestCase):
    def setUp(self):
        self.html = CACHE_DICTION['https://www.826michigan.org/blog/']['html']
        self.blogs = get_blog_list(self.html)
        self.sample_inst = Blog(self.blogs[0]) # an example of 1 BeautifulSoup instance to pass into your class

    def test_blog_constructor(self):
        self.assertIsInstance(self.sample_inst.date_of_month, str)
        self.assertIsInstance(self.sample_inst.day_of_week, str)
        self.assertIsInstance(self.sample_inst.month_year, str)
        self.assertIsInstance(self.sample_inst.url, str)
        self.assertIsInstance(self.sample_inst.title, str)
        self.assertIsInstance(self.sample_inst.description, str)

    def test_blog_convert_date(self):
        self.assertIsInstance(self.sample_inst.convert_date(),str)

    def test_blog_category(self):
        self.assertIsInstance(self.sample_inst.blog_category(),str)

    def test_blog_repr(self):
        self.assertEqual(self.sample_inst.__repr__(), "'NOVEMBER Featured Student Writing' published on 27 November 2017")

    def test_blog_contains(self):
        self.assertTrue("NOVEMBER" in self.sample_inst)
        self.assertTrue("Foundation" not in self.sample_inst)

    def test_list_vars(self):
        self.assertIsInstance(self.blogs,list)

    def test_list_elem_types(self):
        self.assertIsInstance(Blog(self.blogs[0]),Blog)

class Parsing(unittest.TestCase):

    def setUp(self):
        pass

    def test_list_vars(self):
        self.assertIsInstance(blog_list_1,list)
        self.assertIsInstance(blog_list_2, list)
        self.assertIsInstance(blog_list_3, list)

    def test_list_elem_types(self):
        self.assertIsInstance(blog_objs[0],Blog)

class Functions(unittest.TestCase):

    def setUp(self):
        self.f = open("sample_blog_page.html")
        self.html = self.f.read()

    def test_get_and_set_in_cache(self):
        url = "https://www.826michigan.org/about-us/"
        self.assertTrue(get_and_set_in_cache(url))

    def test_get_blog_list(self):
        self.assertTrue(get_blog_list(self.html))

    def test_get_connection_and_cursor(self):
        self.assertTrue(get_connection_and_cursor())

    def test_get_category_id(self):
        cat_id = "Featured Foundation"
        self.assertTrue(get_category_id(cat_id),2)



if __name__ == '__main__':
    unittest.main(verbosity=2)
