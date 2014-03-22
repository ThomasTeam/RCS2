from os import path
import unittest

from comp61542.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

        
    def test_serch_author_by_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "simple.xml"))
        #data = db.search_author_by_name("author1")
        db.search_author_by_name("AUTHOR")

if __name__ == '__main__':
    unittest.main()
