from flask import render_template, url_for, redirect, flash, request
from inventory import app, db
from forms import *
from models import *

@app.route('/')
@app.route('/balance', methods=['GET','POST'])
def balance():
    db.session.query(Balance).delete()
    db.session.commit()
    products = Product.query.all()
    locations = Location.query.all()
    for product in products:
        for location in locations:
            qty_added = db.session.query(db.func.sum(Movement.quantity)).filter(Movement.product==product.name).filter(Movement.to_location==location.name).scalar()
            qty_subtracted = db.session.query(db.func.sum(Movement.quantity)).filter(Movement.product==product.name).filter(Movement.from_location==location.name).scalar()  
            if qty_added is None:
                qty_added = 0
            if qty_subtracted is None:
                qty_subtracted = 0
            balance = qty_added - qty_subtracted
            b = Balance(product=product.name, location=location.name, balance=balance)
            db.session.add(b)
            db.session.commit()

    balance = Balance.query.all()
    return render_template('balance.html', balance=balance)

@app.route('/products', methods=['GET','POST'])
def products():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(name = form.product.data)
        db.session.add(p)
        db.session.commit()
        products = Product.query.all()
        flash("A new product has been added!")
        return render_template('products.html', products=products, form=form)
    products = Product.query.all()
    return render_template('products.html', products=products, form=form)

@app.route('/locations', methods=['GET','POST'])
def locations():
    form = LocationForm()
    if form.validate_on_submit():
        l = Location(name = form.location.data)
        db.session.add(l)
        db.session.commit()
        locations = Location.query.all()
        flash("A new location has been added!")
        return render_template('locations.html', locations=locations, form=form)
    locations = Location.query.all()
    return render_template('locations.html', locations=locations, form=form)

@app.route('/movements', methods=['GET','POST'])
def movements():
    form = MovementForm()
    form.product.choices = [(product.id,product.name) for product in Product.query.all()]

    # Adding the none option
    flag = True
    locations = Location.query.all()
    for location in locations:
        if location.name == "None":
            flag = False
    if flag:
        l = Location(name = "None")
        db.session.add(l)
        db.session.commit()
    form.from_location.choices = [(location.id,location.name) for location in Location.query.all()]
    form.to_location.choices = [(location.id,location.name) for location in Location.query.all()]

    if form.validate_on_submit():
        product = Product.query.filter_by(id=form.product.data).first()
        from_location = Location.query.filter_by(id=form.from_location.data).first()
        to_location = Location.query.filter_by(id=form.to_location.data).first()
        if int((Balance.query.filter_by(product = product.name).filter_by(location = from_location.name).first()).balance) < int(form.quantity.data) and from_location.name != "None":
           flash("Invalid movement. Quantity of the product is insufficient.")
        else: 
            m = Movement(product_id = product.id, product = product.name, from_location_id = from_location.id, from_location = from_location.name, to_location_id = to_location.id, to_location = to_location.name, quantity = form.quantity.data)
            db.session.add(m)
            db.session.commit()
            flash("A new product movement has been added!")
        movements = Movement.query.all()
        products = Product.query.all()
        locations = Location.query.all()
        return render_template('movements.html', movements=movements, products=products, locations=locations, form=form)
    
    movements = Movement.query.all()
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('movements.html', movements=movements, products=products, locations=locations, form=form)

@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])   
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.product.data
        movements = Movement.query.filter_by(product_id=product_id).all()
        for movement in movements:
            movement.product = form.product.data
        db.session.commit()
        flash('The product has been edited!', 'success')
        return redirect(url_for('products'))
    elif request.method == 'GET':
        form.product.data = product.name 
    edit_button = True   
    return render_template('products.html',form=form, edit_button=edit_button)

@app.route('/locations/<int:location_id>/edit', methods=['GET', 'POST'])   
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm()
    if form.validate_on_submit():
        location.name = form.location.data
        movements = Movement.query.filter((Movement.from_location_id == location_id) | (Movement.to_location_id == location_id)).all()
        for movement in movements:
            if movement.from_location_id == location_id:
                movement.from_location = form.location.data
            else:
                movement.to_location = form.location.data
        db.session.commit()
        flash('The location has been edited!', 'success')
        return redirect(url_for('locations'))
    elif request.method == 'GET':
        form.location.data = location.name 
    edit_button = True   
    return render_template('locations.html', form=form, edit_button=edit_button)

@app.route('/movements/<int:movement_id>/edit', methods=['GET', 'POST'])   
def edit_movement(movement_id):
    movement = Movement.query.get_or_404(movement_id)
    form = MovementForm()
    if request.method == 'POST':
        product = Product.query.filter_by(id=form.product.data).first()
        from_location = Location.query.filter_by(id=form.from_location.data).first()
        to_location = Location.query.filter_by(id=form.to_location.data).first()
        if int((Balance.query.filter_by(product = product.name).filter_by(location = from_location.name).first()).balance) < int(form.quantity.data) and from_location.name != "None":
           flash("Invalid movement. Quantity of the product is insufficient.")
        else: 
            movement.product_id = product.id
            movement.product = product.name
            movement.from_location_id = from_location.id
            movement.from_location = from_location.name
            movement.to_location_id = to_location.id
            movement.to_location = to_location.name
            movement.quantity = form.quantity.data
            db.session.commit()
            flash('The product movement has been edited!', 'success')
        return redirect(url_for('movements'))
    elif request.method == 'GET':
        form.product.choices = [(product.id,product.name) for product in Product.query.all()]
        form.from_location.choices = [(location.id,location.name) for location in Location.query.all()]
        form.to_location.choices = [(location.id,location.name) for location in Location.query.all()]
        form.quantity.data = movement.quantity
    edit_button = True   
    return render_template('movements.html',form=form, edit_button=edit_button)

@app.route('/products/<int:product_id>/delete', methods=['GET', 'POST'])   
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    movements = Movement.query.filter_by(product_id=product_id).all()
    for movement in movements:
        db.session.delete(movement)
    db.session.delete(product)
    db.session.commit()
    flash('The product has been deleted!', 'success')
    return redirect(url_for('products'))

@app.route('/locations/<int:location_id>/delete', methods=['GET', 'POST'])   
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    movements = Movement.query.filter((Movement.from_location_id == location_id) | (Movement.to_location_id == location_id)).all()
    for movement in movements:
        db.session.delete(movement)
    db.session.delete(location)
    db.session.commit()
    flash('The location has been deleted!', 'success')
    return redirect(url_for('locations'))

@app.route('/movements/<int:movement_id>/delete', methods=['GET', 'POST'])   
def delete_movement(movement_id):
    movement = Movement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    flash('The product movement has been deleted!', 'success')
    return redirect(url_for('movements'))












