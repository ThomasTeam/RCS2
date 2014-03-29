from os import path
import unittest

from comp61542.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

        
    def test_rank_author_by_contribution_top_one(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        d = db.rank_author_by_contribution()
        for author in d:
           f = d[author][0]
           l = d[author][1] 
           self.assertEqual(author,"Stefano Ceri")
           self.assertEqual(f,86)
           self.assertEqual(l,33)
           break
       
    def test_rank_author_by_contribution_less_one(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        d = db.rank_author_by_contribution("0,1")
        for author in d:
           f = d[author][0]
           l = d[author][1] 
           self.assertEqual(author,"A. Patrick")
           self.assertEqual(f,0)
           self.assertEqual(l,1)
           break  
        
    def test_rank_author_using_search(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_curated_sample.xml"))
        #data = db.search_author_by_name("author1")
        d = db.rank_author_by_contribution("Sean","0,1")
        for author in d:
           f = d[author][0]
           l = d[author][1] 
           self.assertEqual(author,"Sean Bechhofer")
           self.assertEqual(f,11)
           self.assertEqual(l,12)
           break  
       
        
if __name__ == '__main__':
    unittest.main()
