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
        self.assertEqual(db.search_author_by_name("Sara Camai"),[("Sara Camai",15,9,6,0,0,20)])
        
    def test_serch_author_by_name_using_part_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Carl"),[("Carl Kesselman",2,2,0,0,0,2),("Carlo Batini",10,6,2,0,1),("Carlo Conserva",8,8,0,0,0,10),("Carlo Siciliano",2,2,0,0,0,2),("Carlo Zaniolo",1,0,0,0,0,5),("Carlos Eduardo Scheidegger",1,0,1,0,0,45),("Carlos N. Cumberbatch",1,1,0,0,0,2)])
    
    def test_serch_author_by_name_usng_first_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Steffen","1","2"),[("Steffen Mller",1,0,1,0,0,9)])
    
    def test_serch_author_by_name_usng_last_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Steffen","1","3"),[("Bernhard Steffen",1,1,0,0,0,9)])   
         
        
if __name__ == '__main__':
    unittest.main()
