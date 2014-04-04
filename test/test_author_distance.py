from os import path
import unittest

from comp61542.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

        
    def test_get_author_distance_04(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_sorting_example.xml"))
        #data = db.search_author_by_name("author1")
        d = db.get_author_distance(0,4)# Alon Y. Halevy & Philip A. Bernstein
        self.assertEqual(d,"0")
          
    def test_get_author_distance_45(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_sorting_example.xml"))
        #data = db.search_author_by_name("author1")
        d = db.get_author_distance(4,5)# Natalya Fridman Noy & Philip A. Bernstein
        self.assertEqual(d,"X")
          
    def test_get_author_distance_35(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_sorting_example.xml"))
        #data = db.search_author_by_name("author1")
        d = db.get_author_distance(3,5)# Natalya Fridman Noy & Pedro Domingos
        self.assertEqual(d,"1")     
   
        
if __name__ == '__main__':
    unittest.main()
