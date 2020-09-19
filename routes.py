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
    if form.validate_on_submit():
        product = Product.query.filter_by(id=form.product.data).first()
        from_location = Location.query.filter_by(id=form.from_location.data).first()
        to_location = Location.query.filter_by(id=form.to_location.data).first()
        m = Movement(product = product.name, from_location = from_location.name, to_location = to_location.name, quantity = form.quantity.data)
        db.session.add(m)
        db.session.commit()
        movements = Movement.query.all()
        products = Product.query.all()
        locations = Location.query.all()
        return render_template('movements.html', movements=movements, products=products, locations=locations, form=form)
    
    form.product.choices = [(product.id,product.name) for product in Product.query.all()]
    form.from_location.choices = [(location.id,location.name) for location in Location.query.all()]
    form.to_location.choices = [(location.id,location.name) for location in Location.query.all()]
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
        db.session.commit()
        flash('The product has been edited!', 'success')
        return redirect(url_for('products'))
    elif request.method == 'GET':
        form.product.data = product.name 
    edit_button = True   
    return render_template('products.html',form=form, edit_button=edit_button)

@app.route('/products/<int:product_id>/delete', methods=['GET', 'POST'])   
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    movements = Movement.query.filter_by(product_id=product_id).all()
    db.session.delete(movements)
    db.session.commit()
    flash('The product has been deleted!', 'success')
    return redirect(url_for('products'))












