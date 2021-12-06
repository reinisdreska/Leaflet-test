from flask_sqlalchemy import SQLAlchemy
    
db = SQLAlchemy()
    
class place_model(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    description = db.Column(db.Text())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    def __init__(self, place_id, name, description, latitude, longitude):
        self.place_id = place_id
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"{self.name}"