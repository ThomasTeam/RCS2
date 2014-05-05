from os import path
import networkx as nx
import unittest

from comp61542.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")
        #0153462 : ABCDEFG
        
    def test_get_coauthor_graph_A(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_distance_graph.xml"))
        #data = db.search_author_by_name("author1")
        d = db.get_author_coauthors("A")# A => B
       # print [p for p in db.get_author_distance(0,1)]
        self.assertEqual(d,["A","B","G","D","E"])
          
    def test_get_coauthor_graph_C(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_distance_graph.xml"))
        #data = db.search_author_by_name("author1")
        d = db.get_author_coauthors("C")# C => B => D & C => G => D
        self.assertEqual(d,["C","B","G"])

          
    def test_get_coauthor_graph_F(self):
        db = database.Database()
        db.read(path.join(self.data_dir, "dblp_distance_graph.xml"))
        #data = db.search_author_by_name("author1")
        d = db.get_author_coauthors("F")# C => B => A => E & C => G => A =>E
        self.assertEqual(d,["F"])    
           

if __name__ == '__main__':
    unittest.main()
