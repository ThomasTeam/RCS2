from comp61542.statistics import average
from collections import OrderedDict
from collections import deque
import operator
import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]

class Publication:
    CONFERENCE_PAPER = 0  # inproceeding
    JOURNAL = 1  # article
    BOOK = 2  # book    
    BOOK_CHAPTER = 3  # incollection

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors

class Author:
    def __init__(self, name):
        self.name = name

class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2

class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print "Error reading file (" + e.getMessage() + ")"
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def search_author_by_name(self, author, sort="1,1", namepart="1"):
        (_,data) = self.get_publications_by_author()
        cloneData = data[:]
        index = 0
        for authorKey in data:
            if namepart == "1":
                if authorKey[0].lower().find(author.lower()) == -1:
                    del cloneData[index]
                    continue
            else:
                authorNameList = authorKey[0].split()
                if namepart == "2":
                    if authorNameList[0].lower().find(author.lower()) == -1:
                        del cloneData[index]
                        continue
                elif authorNameList[len(authorNameList) - 1].lower().find(author.lower()) == -1: 
                    del cloneData[index]
                    continue   
            index = index + 1
#       resultList = []
#         for authorKey in self.author_idx:
#             if namepart == "1":
#                 if authorKey.find(author) != -1:
#                     resultList.append(authorKey)
#             else:
#                 authorNameList = authorKey.split()
#                 if namepart == "2":
#                     if authorNameList[0].find(author) != -1:
#                         resultList.append(authorKey)
#                 elif authorNameList[len(authorNameList) - 1].find(author) != -1:
#                     resultList.append(authorKey)

        coauthors = {}
        for p in self.publications:
            for a in p.authors:
                for a2 in p.authors:
                    if a != a2:
                        try:
                            coauthors[a].add(a2)
                        except KeyError:
                            coauthors[a] = set([a2])
        for c in cloneData:
            c.append(len(coauthors[self.author_idx.get(c[0])]))
            c.append(self.author_idx.get(c[0]))
            #c.append(len(coauthors[[k for k, v in self.author_idx.iteritems() if v == c[0]][0]]))
        
        sortValues = sort.split(",")          
        #if sortValues[0] == "0": 
        #    return sorted(cloneData,key = lambda row : row[int(sortValues[0])].lower(), reverse= sortValues[1] == "2")
        #else:
        #    return sorted(cloneData,key = lambda row : (row[int(sortValues[0])],row[0].lower()) , reverse= sortValues[1] == "2")
        if sortValues[0] == "0": 
            return sorted(cloneData,key = lambda row : row[0].lower(), reverse= sortValues[1] == "2")
        else:
            sortedData = sorted(cloneData,key = lambda row : row[0].lower())
            return sorted(sortedData,key = lambda row : row[int(sortValues[0])], reverse= sortValues[1] == "2")

    def author_stats_by_id(self, id):
        dataSearch = self.search_author_by_name("","1,1","1")  

        personal = {"Number of publications":[0,0,0,0,0],"Number of times Sole Author":[0,0,0,0,0],"Number of times First Author":[0,0,0,0,0],"Number of times Last Author":[0,0,0,0,0],"Number of Coauthors":[0,0,0,0,0]}
        searchDetails = [] 
        for entry in dataSearch:  
            if id == str(entry[7]):
                searchDetails=entry[:]
                break 
        
        authorName = searchDetails[0]
        for p in self.publications:
            for au in p.authors:
                if str(au) == id:
                    personal["Number of publications"][p.pub_type]+=1
                    for coauthor in p.authors:
                        if au != coauthor:
                            personal["Number of Coauthors"][p.pub_type]+=1
                    break
            if str(p.authors[0]) == id:
                if len(p.authors) == 1:
                    personal["Number of times Sole Author"][p.pub_type]+=1
                else:
                    personal["Number of times First Author"][p.pub_type]+=1
            elif str(p.authors[len(p.authors) - 1]) == id:
                personal["Number of times Last Author"][p.pub_type]+=1
        for item in personal:
            personal[item][4]=personal[item][0]+personal[item][1]+personal[item][2]+personal[item][3]
         #make the sequence suitable for html page
        result = {"Number of publications":[0,0,0,0,0],"Number of times Sole Author":[0,0,0,0,0],"Number of times First Author":[0,0,0,0,0],"Number of times Last Author":[0,0,0,0,0],"Number of Coauthors":[0,0,0,0,0]}
        for item in personal:
            result[item][0]=personal[item][4]
            result[item][1]=personal[item][1]
            result[item][2]=personal[item][0]
            result[item][3]=personal[item][2]
            result[item][4]=personal[item][3]
            
                           
        return authorName,result
 
    def get_author_distance(self,AuthorID1,AuthorID2):
        coauthors = {}
        for p in self.publications:
            for a in p.authors:
                for a2 in p.authors:
                    if a != a2:
                        try:
                            coauthors[a].add(a2)
                        except KeyError:
                            coauthors[a] = set([a2])
        newpath = self.find_shortest_path(coauthors, AuthorID1, AuthorID2)    
        if newpath==None:
            return "x"
        else:
            return str(len(newpath)-2)
    
    
    def find_shortest_path(self,graph, start, goal):
        visited = {start: None}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node == goal:
                path = []
                while node is not None:
                    path.append(node)
                    node = visited[node]
                return path[::-1]
            for neighbour in graph[node]:
                if neighbour not in visited:
                    visited[neighbour] = node
                    queue.append(neighbour)
        return None
    
#    def find_shortest_path(self, graph, start, end, path=[]):
#        path = path + [start]
#        if start == end:
#            return path
#        if not graph.has_key(start):
#            return None
#        shortest = None
#        for node in graph[start]:
#            if shortest==0:
#                return shortest
#            if node not in path:
#                newpath = self.find_shortest_path(graph, node, end, path)
#                if newpath: 
#                    if not shortest or len(newpath) < len(shortest):
#                        shortest = newpath
#                        
#        return shortest
    
    
            
    def get_all_authors(self):  
        return self.author_idx.keys()

    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        data = []
        for a in coauthors:
            data.append([ display(self, coauthors, a),
                ", ".join([
                    display(self, coauthors, ca) for ca in coauthors[a] ]) ])

        return (header, data)

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ func(auth_per_pub[i]) for i in np.arange(4) ] + [ func(list(itertools.chain(*auth_per_pub))) ]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(pub_per_auth[:, i]) for i in np.arange(4) ] + [ func(pub_per_auth.sum(axis=1)) ]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(4) ] + [ func(ystats.sum(axis=1)) ]
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [ [set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1) ]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([ [ len(S) for S in y ] for y in yauth ])

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(5) ]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
                + [ func(auth_per_pub[i]) for i in np.arange(4) ]
                + [ func(list(itertools.chain(*auth_per_pub))) ],
            [name + " publications per author"]
                + [ func(pub_per_auth[:, i]) for i in np.arange(4) ]
                + [ func(pub_per_auth.sum(axis=1)) ] ]
        return (header, data)

    def rank_author_by_contribution(self, author = "", rank="0,2", pub = "0"):
        returnResult = {}
        d = {}
        FirstAuthor = []
        LastAuthor = []
        SoleAuthor = []

        if pub == "0":
            pub =-1
        elif pub == "1":
            pub = 1
        elif pub == "2":
            pub = 0
        elif pub == "3":
            pub = 2
        elif pub == "4":
            pub = 3


        for p in self.publications:
            if pub == -1 or p.pub_type == pub:
                if len(p.authors) == 1:
                    SoleAuthor.append(p.authors[0]) 
                else:
                    FirstAuthor.append(p.authors[0])
                    LastAuthor.append(p.authors[len(p.authors) - 1]) 
  
        for item in FirstAuthor:
            if d.has_key(item):
                d[item][0] += 1
            else:
                d[item] = [1,0,0,item]
                
        for item in LastAuthor:
            if d.has_key(item):
                d[item][1] += 1
            else: 
                d[item] = [0,1,0,item]

        for item in SoleAuthor:
            if d.has_key(item):
                d[item][2] += 1
            else:
                d[item] = [0,0,1,item]
        # cc = sorted(d, key=d.get, reverse=(rank=="1"))
        #if author != "": 
        for c in d:
            if not author or author.isspace() or author is None or len(author) == 0:
                returnResult[self.authors[c].name]= d[c]
                continue
            elif self.authors[c].name.lower().find(author.lower()) != -1:
                returnResult[self.authors[c].name]= d[c]
           # else:
           #    returnResult[self.authors[c].name]= d[c]
            
        rankValues = rank.split(",")
        sorted_x = OrderedDict(sorted(returnResult.items(), key=lambda t:t[0]))
        return OrderedDict(sorted(sorted_x.items(), key=lambda t:t[1][int(rankValues[0])],reverse = rankValues[1] == "2"))
        

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "Total")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [ len(a) for a in alist ] + [len(ua)] ]
        return (header, data)

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "All publications")

        astats = [ [[], [], [], []] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [self.authors[i].name]
            + [ func(L) for L in astats[i] ]
            + [ func(list(itertools.chain(*astats[i]))) ]
            for i in range(len(astats)) ]
        return (header, data)


    def get_publications_by_author(self):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")
        astats = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1
        
        data = [ [self.authors[i].name] + astats[i] + [sum(astats[i])] #+ [self.authors[i]]
            for i in range(len(astats)) ]
        return (header, data)

    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(L) for L in ystats[y] ]
            + [ func(list(itertools.chain(*ystats[y]))) ]
            for y in ystats ]
        return (header, data)

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [ [y] + ystats[y] + [sum(ystats[y])] for y in ystats ]
        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(ystats[y][:, i]) for i in np.arange(4) ]
            + [ func(ystats[y].sum(axis=1)) ]
            for y in ystats ]
        return (header, data)

    def get_author_totals_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [ [y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
            for y in ystats ]
        return (header, data)

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print "Warning: excluding publication due to missing information"
            print "    Publication type:", PublicationType[pub_type]
            print "    Title:", title
            print "    Year:", year
            print "    Authors:", ",".join(authors)
            return
        if title == None:
            print "Warning: adding publication with missing title [ %s %s (%s) ]" % (PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [ (self.authors[key].name, data[key])
            for key in data ]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [ [self.authors[i].name, -1] for i in range(na) ]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = [ "sub", "sup", "i", "tt", "ref" ]
    PUB_TYPE = {
        "inproceedings":Publication.CONFERENCE_PAPER,
        "article":Publication.JOURNAL,
        "book":Publication.BOOK,
        "incollection":Publication.BOOK_CHAPTER }

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs
