from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    product = StringField("Product", validators=[DataRequired()])
    add_product = SubmitField("Add Product")

class LocationForm(FlaskForm):
    location = StringField("Location", validators=[DataRequired()])
    add_location = SubmitField("Add Location")

class MovementForm(FlaskForm):
    product = SelectField("Product", choices = [])
    from_location = SelectField("From Location", coerce=int)
    to_location = SelectField("To Location", coerce=int)
    quantity = StringField("Quantity", validators=[DataRequired()])
    add_movement = SubmitField("Add Movement")

