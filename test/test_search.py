from os import path
import unittest

from comp61542.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

        
    def test_serch_author_by_name_using_full_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Stefano Ceri"),["Stefano Ceri"])
        
    def test_serch_author_by_name_using_part_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Carl"),["Carl Kesselman","Carlo Batini","Carlo Conserva","Carlo Siciliano","Carlo Zaniolo","Carlos Eduardo Scheidegger","Carlos N. Cumberbatch"])
    
    def test_serch_author_by_name_usng_first_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Steffen","1","2"),["Steffen Mller"])
    
    def test_serch_author_by_name_usng_last_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Steffen","1","3"),["Bernhard Steffen"])    
         
        
if __name__ == '__main__':
    unittest.main()
