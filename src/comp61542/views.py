from comp61542 import app
from database import database
from flask import (render_template, request, url_for, redirect)

def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([ (fmt % i).rstrip('0').rstrip('.') for i in item ]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result

@app.route('/')
def root():
    print url_for('static', filename='home.html')
    return redirect(url_for('static', filename='home.html')) #app.send_static_file('home.html')



@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"averages"}
    args['title'] = "Averaged Data"
    args['path'] = "Publication"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [ database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE ]
    tables.append({
        "id":1,
        "title":"Average Authors per Publication",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_per_publication(i)[1])
                for i in averages ] })
    tables.append({
        "id":2,
        "title":"Average Publications per Author",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_per_author(i)[1])
                for i in averages ] })
    tables.append({
        "id":3,
        "title":"Average Publications in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_in_a_year(i)[1])
                for i in averages ] })
    tables.append({
        "id":4,
        "title":"Average Authors in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_in_a_year(i)[1])
                for i in averages ] })


    args['tables'] = tables
    return render_template("averages.html", args=args)

@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"coauthors"}
    args["title"] = "Co-Authors"
    args['path'] = "Author"
    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    return render_template("coauthors.html", args=args)

#@app.route("/")
#def showStatisticsMenu():
#    dataset = app.config['DATASET']
#    args = {"dataset":dataset}
#    return render_template('statistics.html', args=args)

@app.route("/collaboration")
def getCollaborationPage():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset}
    args["method"] = "GET"
    args["title"] = "Authors Collaboration"
    args['path'] = "Author"
    args["data"] = []
    args["authors"] = db.author_idx
    args["aid1"] = 0
    args["aid2"] = 0
    return render_template('Author_Collaboration.html', args=args)

@app.route("/collaboration", methods = ['POST'])
def postCollaborationPage():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset}
    args["method"] = "POST"
    args["title"] = "Authors Collaboration"
    args['path'] = "Author"
    args["authors"] = db.author_idx
    args["aid1"] = request.form['aid1']
    args["aid2"] = request.form['aid2']
    args["data"] = db.get_author_distance(int(request.form['aid1']),int(request.form['aid2']))
    return render_template('Author_Collaboration.html', args=args)

@app.route("/search/author")
def getSearchPage():
    
    dataset = app.config['DATASET']
    args = {"dataset":dataset}
    args["method"] = "GET"
    args['path'] = "Author"
    args["title"] = "Search author by name"
    return render_template('search_details.html', args=args)  

@app.route("/search/author", methods = ['POST'])
def postSearchPage():
    
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "search":request.form['search'],"sort":request.form['sort'], "name":request.form['name']}
    args["method"] = "POST"
    args['path'] = "Author"
    args["title"] = "Search by author name"
    args["data"] = db.search_author_by_name(request.form['search'],request.form['sort'], request.form['name'])
    return render_template('search_details.html', args=args)     

@app.route("/ranking")
def rankingAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "sort":"0,2", "query":"", "publication":"0"}
    args["title"] = "Author Ranking"
    args['path'] = "Author"
    args["header"] = ["Author", "First Author", "Last Author"]
    args["data"] = db.rank_author_by_contribution( )  #first or manager
    return render_template('author_ranking.html', args=args)  

@app.route("/ranking", methods = ['POST'])
def poatRankingAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "query":request.form["search"], "publication":request.form["pub"]}
    args["title"] = "Author Ranking"
    args['path'] = "Author"
    args["header"] = ["Author", "First Author", "Last Author"]
    args["data"] = db.rank_author_by_contribution(request.form["search"],request.form["sort"],request.form["pub"])
    #first or manager
    args["sort"] = request.form['sort']
    return render_template('author_ranking.html', args=args)  

@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}

    if (status == "publication_summary"):
        args["path"] = "Publication"
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()

    if (status == "publication_author"):
        args["path"] = "Publication"
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author()

    if (status == "publication_year"):
        args["path"] = "Publication"
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()

    if (status == "author_year"):
        args["path"] = "Author"
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()

    return render_template('statistics_details.html', args=args)

@app.route("/stats/<query>")
def individualAuthorStats(query):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":query}
    args["title"] = "Inidividual Details"
    args["path"] = "Author"
    args["author"],args["data"] = db.author_stats_by_id(request.args.get("id"))  
    return render_template('individual_details.html', args=args)  