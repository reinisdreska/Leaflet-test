#py -m flask run
from flask import Flask, render_template, request, redirect
from model import db, place_model

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("map.html")

    if request.method == "POST":
        place_id = request.form["place_id"]
        name = request.form["name"]
        description = request.form["description"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        place = place_model(
            place_id=place_id, name=name, description=description, latitude=latitude, longitude=longitude
        )
        db.session.add(place)
        db.session.commit()
        return redirect("/data")

@app.route("/data")
def RetrieveList():
    places = place_model.query.all()
    return render_template("datalist.html", places=places)

@app.route("/data/<int:id>")
def RetrieveEmployee(id):
    place = place_model.query.filter_by(place_id=id).first()
    return render_template("data.html", place=place)