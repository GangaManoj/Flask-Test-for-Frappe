from inventory import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    product_movements = db.relationship('Movement', backref='item', lazy=True)

    def __repr__(self):
        return f"{self.name} added."

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    #changes_in_location = db.relationship('Movement', backref='location', lazy=True)
    from_loc = db.relationship('Movement', backref='to', lazy=True, primaryjoin='Movement.from_location_id == Location.id')
    to_loc = db.relationship('Movement', backref='from', lazy=True, primaryjoin='Movement.to_location_id == Location.id')


    def __repr__(self):
        return f"{self.location} added."

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.Column(db.String(50), nullable=False)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    from_location = db.Column(db.String(50))
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    to_location = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.quantity} units of {self.product} moved from {self.from_location} to {self.to_location} at {self.timestamp}."

class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    #qty_added = db.Column(db.Integer)
    #qty_subtracted = db.Column(db.Integer)
    balance = db.Column(db.Integer)



   