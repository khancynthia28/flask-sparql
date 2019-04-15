from flask import Flask, render_template, request
import rdflib

g = rdflib.Graph()
g.parse("nobeldata.owl")
print("graph has %s statements." % len(g))

app = Flask(__name__)

@app.route("/")
def home():
    nationality = nations()
    category = categories()
    years = year()
    return render_template("index.html", nationality=nationality, categories = category, years = years)

@app.route("/nobel/categories")
def categories():
#GET: Return sorted names of all nobel categories
    qres = g.query(
            """
            PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
            SELECT ?w
            {
                    ?g rdf:type table:PersonWinner;
                    table:WonPrize ?w.
                    }
            GROUP BY ?w
            ORDER BY ?w""")

    unique_category = []
    for row in qres:
        category = ("%s" % row).split('/')[-4]
        if category not in unique_category:
            unique_category.append(category)

    return unique_category

@app.route("/nobel/years")
def year():
#GET: Return sorted years nobels are awarded
    qres = g.query(
            """
            PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
            SELECT ?w
            {
                    ?g rdf:type table:PersonWinner;
                    table:WonPrize ?w.
                    }
            GROUP BY ?w
            ORDER BY ?w""")

    unique_year = []

    for row in qres:
        year = ("%s" % row).split('/')[-2]
        if year not in unique_year:
            unique_year.append(year)

    unique_year.sort()

    return unique_year

@app.route("/nobel/nations")
def nations():
#GET: Return sorted names of all nations
    qres = g.query(
            """
            PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
            SELECT ?n
            {
                    ?g rdf:type table:PersonWinner;
                    table:nationality ?n.
                    }
            GROUP BY ?n
            ORDER BY ?n""")

    nation = []
    for row in qres:
        name = ("%s" % row).rsplit('/',1)[-1]
        nation.append(name)

    return nation


@app.route("/nobel/getYear", methods=['GET', 'POST'])
def getYear():
#GET: Return list of all nobel winners for the given year
    year = request.form.get('year')

    qres = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?n
        {
        ?g rdf:type table:PersonWinner;
        table:name ?n;
        table:WonPrize ?w.
        ?w table:yearWon ?y.
        FILTER (?y = """ + str(year) + """)
        }""")

    winners = []
    for row in qres:
        winners.append("%s" % row)

    return render_template("winners.html", winners=winners)

@app.route("/nobel/getNation", methods=['GET', 'POST'])
def getNation():
#GET: Return list of all nobel winners for the given nation
    nation = request.form.get('nationality')

    qres = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?n ?d
        {
            ?g rdf:type table:PersonWinner;
            table:name ?n;
            table:nationality ?d.
        }""")

    winners = []
    for row in qres:
        if nation in ("%s %s" % row):
            winners.append(("%s %s" % row).split("http",1)[0])

    return render_template("winners.html", winners = winners)

@app.route("/nobel/getCategory", methods=['GET', 'POST'])
def getCategory():
#GET: Return list of all nobel winners for the given nation
    category = request.form.get('category')
    qres = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?n ?w
        {
            ?g rdf:type table:PersonWinner;
            table:name ?n;
            table:WonPrize ?w.
        }
        GROUP BY ?w
        ORDER BY ?w""")


    winners = []
    for row in qres:
        if category in ("%s %s" % row):
            winners.append(("%s %s" % row).split("http", 1)[0])

    return render_template("winners.html", winners = winners)

@app.route("/nobel/getYearCategory", methods=['GET', 'POST'])
def getYearCategory():
#GET: Return list of all nobel winners for the given year and category
    category = request.form.get('category')
    year = str(request.form.get('year'))
    qres = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?n ?w ?y
        {
            ?g rdf:type table:PersonWinner;
            table:name ?n;
            table:WonPrize ?w.
            ?w table:yearWon ?y.
        }
        GROUP BY ?w
        ORDER BY ?w""")

    winners = []
    for row in qres:
        if (category in ("%s %s %s" % row)) and (year in ("%s %s %s" % row)):
            winners.append(("%s %s %s" % row).split("http", 1)[0])


    return render_template("winners.html", winners=winners)

@app.route("/getDetails/<string:name>")
def getDetails(name):
#GET: Return details of the given nobel winner
    name = name
    qres = g.query(
    """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT ?n ?nt ?b ?p ?w ?y
    {
        ?g rdf:type table:PersonWinner;
        table:name ?n;
        table:nationality ?nt;
        table:birthYear ?b;
        table:photo ?p;
        table:WonPrize ?w.
        ?w table:yearWon ?y;
        
    }
    """)
    result = {
        "name": name,
        "nationality": 'not found',
        "category": 'not found',
        "year": 0000,
        "association": 'not found',
        "born": 0000,
        "died": 0000,
        "motivation": 'not found',
        "photo": 'not found'
    }
    for row in qres:
        if name in str(row.asdict()['n'].toPython()):
            #result["association"] = str(row.asdict()['a'].toPython()).split('#',1)[-1]
            result["nationality"] = str(row.asdict()['nt'].toPython()).split('/')[-1]
            result["born"] = str(row.asdict()['b'].toPython())
            #result["died"] = str(row.asdict()['d'].toPython())
            result["photo"] = str(row.asdict()['p'].toPython())
            #result["motivation"] = str(row.asdict()['m'].toPython())
            result["category"] = str(row.asdict()['w'].toPython()).split('/')[-4]
            result["year"] = str(row.asdict()['y'].toPython())


    qres2 = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?n ?a
            {
                ?g rdf:type table:PersonWinner;
                table:name ?n;
                table:Association ?a.
            }

        """)

    for row in qres2:
        if name in str(row.asdict()['n'].toPython()):
            result["association"] = str(row.asdict()['a'].toPython()).split('#',1)[-1]


    qres3 = g.query(
    """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT ?n ?d
        {
            ?g rdf:type table:PersonWinner;
            table:name ?n;
            table:deathYear ?d.
        }

    """)


    for row in qres3:
        if name in str(row.asdict()['n'].toPython()):
            result["died"] = str(row.asdict()['d'].toPython())


    qres4 = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?n ?m
        {
            ?g rdf:type table:PersonWinner;
            table:name ?n;
            table:WonPrize ?w.
        ?w table:motivation ?m;
        }

        """)

    for row in qres4:
        if name in str(row.asdict()['n'].toPython()):
            result["motivation"] = str(row.asdict()['m'].toPython())

    return render_template("details.html", name=name, association=result["association"], nationality=result["nationality"], born=result["born"], died=result["died"], photo=result["photo"], motivation=result["motivation"], category=result["category"], year=result["year"] )

if __name__ == "__main__":
    app.run()
