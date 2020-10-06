from inventory import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    moved_product = db.relationship('Movement', backref='item', lazy=True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    from_loc = db.relationship('Movement', backref='to', lazy=True, primaryjoin='Movement.from_location_id == Location.id')
    to_loc = db.relationship('Movement', backref='from', lazy=True, primaryjoin='Movement.to_location_id == Location.id')

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.Column(db.String(50), nullable=False)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    from_location = db.Column(db.String(50))
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    to_location = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)   