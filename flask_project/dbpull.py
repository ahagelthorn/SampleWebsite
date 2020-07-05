from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

'''
Name of file - dbpull.py

Purpose of file - This file pulls from the database and hosts the site.

Date of most recent revision - 6/2/20

Author(s) - Andrew Hagelthorn, Matt Hurm, Ethan Bradway

Dependencies and Modules - Flask, sqlite3, Jinja2

'''

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///periodicTable.sqlite3"  # configures SQLalchemy to the database. database.db is not used because it lacks the ElementType field
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "False"
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)  # searches without having to list columns


class Table(db.Model):
    __tablename__ = "periodicTable"
    # following line makes file editable
    __table_args__ = {"extend_existing": True}
    rowid = db.Column(db.Text, primary_key=True)  # searches lines by rowid


@app.route("/", methods=["post", "get"])
def index():
    def febn(number):
        """
        Parameters - An integer, which is the atomic number of the desired element.

        Return Data - The value corresponding to the provided atomic number.

        Purpose - This method returns the value corresponding to the provided atomic number.

        Pre-conditions and post-conditions - N/A
        """
        return Table.query.filter_by(atomicNumber=str(number)).first()

    # IDK how to apply functions to text
    def to_type_style(eltype):
        """
            Parameters - A string which is a type of element.

            Return Data - The value corresponding to the provided element type.

            Purpose - This method returns the CSS decorator that corresponds to the provided element type.

            Pre-conditions and post-conditions - N/A
        """
        translator = {
            "Hydrogen": "hyd",
            "Alkalai Metal": "akm",
            "Alkaline Earth Metal": "aem",
            "Transition Metal": "tsm",
            "Post-Transition Metal": "ptm",
            "Metalloid": "oid",
            "Nonmetal": "nom",
            "Halogen": "hal",
            "Noble Gas": "nog",
            "Lanthanide": "lan",
            "Actinide": "act",
            "": "unc",
        }  # none given = unclassified = gray box
        for key in translator:
            if eltype == key:
                return translator[key]
        return eltype

    # doesnt work most of the time, no idea why
    def toElStyle(typ, symbol):
        """
        Parameters - A string that is the element type, and another string that is an atomic symbol.

        Return Data - A string that is used as a CSS class.

        Purpose - This method takes elementType and atomicSymbol to create a CSS style definition, i.e. (el akm Li) (inherit from the element, alkalai metal, and lithium style sheets)

        Pre-conditions and post-conditions - N/A
        """
        short_type = to_type_style(typ)
        return "el {} {}".format(short_type, symbol)

    app.jinja_env.globals.update(toElStyle=toElStyle)

    if request.method == "POST":
        # deals with case sensitivity + extra spaces
        element = (request.form.get("element")).strip().lower().title()
        if element is not None:
            return redirect(url_for("moreinfo", slug=element))
        else:
            print("ERROR: ELEMENT NULL")
    app.jinja_env.globals.update(
        febn=febn
    )  # following line is to add a function to jinja2

    # https://www.python.org/dev/peps/pep-0274/
    # https://www.geeksforgeeks.org/python-adding-k-to-each-element-in-a-list-of-integers/
    # main_group_1, main_group_2, synthetic_elements = (
    #     [1] + [3, 11, 19, 37, 57, 87],
    #     [],
    #     [],
    # )
    # main_group_1 += list(map(lambda i: i + 1, main_group_1[1:])) + [21, 39]
    # # https://realpython.com/python-lambda/
    # for j in range(9):
    #     main_group_1 += list(map((lambda i: i + j), [22, 40, 72, 104]))
    # for j in range(5):
    #     main_group_2 += list(map((lambda i: i + j), [5, 13, 31, 49, 81, 113]))
    # main_group_2 += [2, 10, 18, 36, 54, 86, 118]
    # for j in range(14):
    #     synthetic_elements += list(map((lambda i: i + j), [57, 89]))

    return render_template("main.html")  # calls the html file

    """ <!-- {{%for i in main_group_1%}}
        <button type="submit" formaction="#moreinfo"
            onclick="window.location.href = '/moreinfo/{{febn(i).elementName}}';" class="{{ toElStyle(febn(i).elementType, febn(i).atomicSymbol) }}">
            <div class="el_num">{{febn(i).atomicNumber}}</div>
            <div class="el_weight">{{febn(i).atomicMass}}</div>
            <div class="el_sym">{{febn(i).atomicSymbol}}</div>
            <div class="el_name">{{febn(i).elementName}}</div>
        </button>
        {{%endfor%}} -->"""


@app.route("/accessibility")
def page_access():
    """
    Parameters - N/A

    Return Data - The template accessibility.html.

    Purpose - This method renders the "accessibility" template onto the localhost URL.

    Pre-conditions and post-conditions - N/A
    """
    return render_template("accessibility.html")


@app.route("/help")
def page_help():
    """
    Parameters - N/A

    Return Data - The template help.html.

    Purpose - This method renders the "help" template onto the localhost URL.

    Pre-conditions and post-conditions - N/A
    """
    return render_template("help.html")


@app.route("/about")
def page_about():
    """
    Parameters - N/A

    Return Data - The template about.html.

    Purpose - This method renders the "about" template onto the localhost URL.

    Pre-conditions and post-conditions - N/A
    """
    return render_template("about.html")


@app.route("/contact")
def page_contact():
    """
    Parameters - N/A

    Return Data - The template contact.html.

    Purpose - This method renders the "contact" template onto the localhost URL.

    Pre-conditions and post-conditions - N/A
    """
    return render_template("about.html")


@app.route("/moreinfo/<slug>")
def moreinfo(slug):
    """
    Parameters - A slug object

    Return Data - The template corresponding to the provided slug.

    Purpose - This example renders template corresponding to the provided slug onto the localhost URL.

    Pre-conditions and post-conditions - N/A
    """
    element = Table.query.filter_by(elementName=slug).first()
    return render_template("more_info.html", element=element)


if __name__ == "__main__":
    app.run(debug=False)
