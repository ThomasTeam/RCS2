from os import path
import unittest

from comp61542.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

        
    def test_author_stats_by_id(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        name,d = db.author_stats_by_id("5")
        self.assertEqual(name, "Adalberto Zordan")
        counter = 1
        for author in d:
           overall = d[author][0]
           journal = d[author][1] 
           conference = d[author][2]
           book = d[author][3]
           bookChapter = d[author][4]
           if counter == 1: # testing for author overall                     
               self.assertEqual(overall,1)
               self.assertEqual(journal,1)
               self.assertEqual(conference,0)
               self.assertEqual(book,0)
               self.assertEqual(bookChapter,0)
           elif counter == 2: # testing for first author                      
               self.assertEqual(overall,0)
               self.assertEqual(journal,0)
               self.assertEqual(conference,0)
               self.assertEqual(book,0)
               self.assertEqual(bookChapter,0)
           elif counter == 3: # testing for last author                      
               self.assertEqual(overall,1)
               self.assertEqual(journal,1)
               self.assertEqual(conference,0)
               self.assertEqual(book,0)
               self.assertEqual(bookChapter,0)
           elif counter == 4: # testing for sole author                      
               self.assertEqual(overall,0)
               self.assertEqual(journal,0)
               self.assertEqual(conference,0)
               self.assertEqual(book,0)
               self.assertEqual(bookChapter,0)        
           break
          
        
if __name__ == '__main__':
    unittest.main()
