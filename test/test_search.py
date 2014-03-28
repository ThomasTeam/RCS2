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
        self.assertEqual(db.search_author_by_name("Sara Comai"),[["Sara Comai",9,6,0,0,15,20]])
        
    def test_serch_author_by_name_using_part_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Carl"),[["Carlo Zaniolo",0,0,1,0,1,5],["Carlos Eduardo Scheidegger",0,1,0,0,1,49],["Giancarlo Martella",1,1,0,0,2,2],["Carlos N. Cumberbatch",1,0,0,0,1,2],["Carlo Siciliano",1,0,0,0,1,2],["Carlo Conserva", 2, 0, 0, 0, 2, 10],["Carl Kesselman",2,0,0,0,2,2],["Carlo Batini", 6, 3, 1, 0, 10, 15]])
    
    def test_serch_author_by_name_usng_first_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Steffen","1,1","2"),[["Steffen Mller",0,1,0,0,1,9]])
    
    def test_serch_author_by_name_usng_last_name(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Steffen","1,1","3"),[["Bernhard Steffen",1,0,0,0,1,9]])   
     
    def test_serch_author_by_name_sorting_equals(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        self.assertEqual(db.search_author_by_name("Carl","2,1","1"),[["Carlo Zaniolo",0,0,1,0,1,5],["Carlos Eduardo Scheidegger",0,1,0,0,1,49],["Carlo Siciliano",1,0,0,0,1,2],["Carlos N. Cumberbatch",1,0,0,0,1,2],["Giancarlo Martella",1,1,0,0,2,2],["Carl Kesselman",2,0,0,0,2,2],["Carlo Conserva", 2, 0, 0, 0, 2, 10],["Carlo Batini", 6, 3, 1, 0, 10, 15]])
        
        
if __name__ == '__main__':
    unittest.main()
