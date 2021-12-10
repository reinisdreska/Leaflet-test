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
        place_array = []
        if len(place_model.query.all()) > 0:
            for i in range(len(place_model.query.all())):
                place = place_model.query.filter_by(id=i+1).first()
                place_info = {"name":place.name, "description":place.description, "latitude":place.latitude, "longitude":place.longitude}
                place_array.append(place_info)

        return render_template("map.html", place_array=place_array)

@app.route("/add", methods=["GET", "POST"])
def add_track():
    if request.method == "GET":
        return render_template("add.html", title="Add track")

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        place = place_model(
            name=name, description=description, latitude=latitude, longitude=longitude
        )
        db.session.add(place)
        db.session.commit()
        return redirect("/")

@app.route("/data")
def RetrieveList():
    places = place_model.query.all()
    return render_template("datalist.html", places=places, title="Data")

@app.route("/data/<int:id>")
def RetrieveEmployee(id):
    place = place_model.query.filter_by(id=id).first()
    return render_template("data.html", place=place)

@app.route("/data/<int:id>/update", methods=["GET", "POST"])
def update(id):
    place = place_model.query.filter_by(id=id).first()
    if request.method == "POST":
        if place:
            db.session.delete(place)
            db.session.commit()
            name = request.form["name"]
            description = request.form["description"]
            latitude = request.form["latitude"]
            longitude = request.form["latitude"]
            place = place_model(
                name=name, description=description, latitude=latitude, longitude=longitude)
            db.session.add(place)
            db.session.commit()
            return redirect(f"/data")

    return render_template("update.html", place=place, title="Update")