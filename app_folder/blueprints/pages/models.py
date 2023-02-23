from app_folder.extensions import db


class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)



class Newsletter(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String, nullable=False)