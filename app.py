from flask import Flask, render_template, request, url_for, session
import math
import os

app = Flask(__name__)
app.secret_key = "kilcek"


@app.route("/")
def home():
    return render_template("index.html", title = "Home", tools = return_tools())

def return_tools():
    return[
        {"name":"Domů", "route":"/"},
        {"name":"Mocniny", "route":"/mocnina"},
        {"name":"Články", "route":"/clanky"},
        {"name":"Galerie", "route":"/gallery"}
    ]

@app.route("/loguot")
def loguot():
    del session["uzivatel"]
    return render_template("status.html", title="Stav", tools=return_tools())

@app.route("/login",methods=["POST","GET"])
def login():
    valid = 0
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        
        if name == "gres" and password == "admin":
            session["uzivatel"] = name
            return render_template("index.html", title = "Home", tools = return_tools())
        else:
            valid = 1
    
    return render_template("login.html", title = "Login", tools = return_tools(), valid = valid)


@app.route("/gallery")
def gallery():
    files = os.listdir("static/gallery")

    return render_template("gallery.html", title="Galerie", tools=return_tools(), file=files)

@app.route("/gallery/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        try:
            f = request.files["soubor"]
            f.save("static/gallery/"+f.filename)
        except:
            pass
    return render_template("status.html", title="Stav", tools=return_tools())

@app.route("/clanky")
def clanky():
    clanky = vrat_clanky()
    return render_template("clanky.html", articles=clanky, tools = return_tools(), title="Články")

def vrat_clanky():
    return [
        {"nadpis": "První Článek","author":"Pavel", "text": "Toto je text članku."},
        {"nadpis": "Druhy Článek","author":"Pavel", "text": "Toto je text članku."},
        {"nadpis": "Třetí Článek","author":"Pavel", "text": "Toto je text članku."}
    ]
@app.route("/mocnina")
def mocnina():
    return render_template("vypocet.html", tools = return_tools())

@app.route("/vypocet", methods=["POST"])
def vypocet():
    try:
        a = request.form["a"]
        x = request.form["x"]
        moc = int(a) ** int(x)
    except:
        return "kokote!"
    return render_template("vypocet.html", data=moc, tools = return_tools())


""" @app.route("/mocnina/<int:a>/<int:b>")
@app.route("/mocnina/<float:a>/<float:b>")
def mocnina(a, b):
    return f"{a} na {b} je {a**b}" """


@app.route("/sqr/<int:a>")
@app.route("/sqr/<float:a>")
def sqroot(a):
    return f"druhá odmocnina čisla {a} je {math.sqrt(a)}"


if __name__ == "__main__":
    app.run(debug=True)
