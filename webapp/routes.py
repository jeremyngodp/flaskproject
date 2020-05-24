import os, secrets
from PIL import Image
from webapp.forms import LoginForm, EditDish, EditCategory, AddCategory, AddDish
from webapp.models import Category, Dish
from flask import render_template, request, redirect, url_for, flash, session
from webapp import app, db



##################################################################
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', page_title = "Home Page", 
                                        username= session['username'])

    return render_template('index.html', page_title = "Home Page")


##################################################################
@app.route('/login', methods = ["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.username.data == 'phucngo' and form.password.data == '123':
                flash('Login successful', 'success')
                session['username'] = request.form['username']
                return redirect(url_for('staff'))
            else:
                flash('Login Unsuccessful!', 'danger')

    return render_template('login.html', page_title = 'Login', form = form)


##################################################################
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))

@app.route('/staff')
def staff():
    if 'username' in session:
        return render_template('staff.html', username = session['username'], 
                                page_title = 'Staff Area')
    else:
        return redirect(url_for('login'))


##################################################################
@app.route('/staff/editdish/<int:dish_id>', methods = ["POST", "GET"])
def editdish(dish_id):
    form = EditDish()

    current_dish = Dish.query.filter_by(id = dish_id).first()
    if request.method =="POST":
        if form.validate_on_submit():
            current_dish.name = form.name.data
            current_dish.ingredient = form.ingredient.data
            current_dish.price = form.price.data
            current_dish.cat_id = form.cat_name.data
            
            if form.image.data:
                image_name = save_image(form.image.data)
                current_dish.image = image_name

            db.session.commit()
            flash('Dish updated successfully!')
            return redirect(url_for('menu'))
           
    else:
        if 'username' in session:
            return render_template('editdish.html', form = form, username = session['username'], 
                                    current_dish = current_dish)
        
        else:
            flash("Please Login First", 'danger')
            return redirect(url_for('login'))


##################################################################
@app.route('/staff/editcategory/<int:cat_id>', methods = ["POST", "GET"])
def editcategory(cat_id):
    form = EditCategory()
    current_cat = Category.query.filter_by(id = cat_id).first()
    if request.method =="POST":
        if form.validate_on_submit():
            current_cat.cat_name = form.cat_name.data
            db.session.commit()

            flash('Category {} has been updated to {}'.format(current_cat.cat_name, form.cat_name.data))
            return redirect(url_for('menu'))
    else:
        if 'username' in session:
            return render_template('editcategory.html', form = form,
                                    username = session['username'], current_cat = current_cat)
        
        else:
            flash("Please Login First", 'danger')
            return redirect(url_for('login'))


##################################################################
@app.route('/staff/addcategory', methods = ["POST", "GET"])
def addcategory():
    form = AddCategory()

    if request.method == "POST":
        if form.validate_on_submit():
            cat_name = form.name.data

            new_cat = Category(cat_name = cat_name)
            db.session.add(new_cat)
            db.session.commit()
            flash('Category {} added'.format(cat_name))
            
        else:
            flash("Adding new Category unsuccessful")

        return redirect(url_for('menu'))
    else:
        if 'username' in session:
            return render_template('addcategory.html', form = form,
                                    username = session['username'])
        
        else:
            flash("Please Login First", 'danger')
            return redirect(url_for('login'))


##################################################################
# This function will save the image to the folder in the application package
def save_image(form_image):
    # use random hex for file name to improve security and avoid duplicate filenames
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    img_name = random_hex + f_ext
    img_path = os.path.join(app.root_path, 'static/dish_img', img_name)
    
    output_size =(125,125)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(img_path)

    return img_name


##################################################################
@app.route('/staff/adddish', methods = ["POST", "GET"])
def adddish():
    form = AddDish()

    if request.method == "POST":
        if form.validate_on_submit():
            dish_name = form.name.data
            ingredient = form.ingredient.data
            cat_id = form.cat_name.data
            price = int(form.price.data)

            if form.image.data:
                image_name = save_image(form.image.data)
            
            new_dish = Dish(name = dish_name, ingredient = ingredient, price = price, cat_id = cat_id, image = image_name)
            db.session.add(new_dish)
            db.session.commit()
            
            flash('Dish {} added to Category number {}'.format(dish_name, cat_id))
            
        else:
            flash("Adding new dish unsuccessfull")

        return redirect(url_for('menu'))

    else:
        if 'username' in session:
            return render_template('adddish.html', form = form,
                                    username = session['username'])
        
        else:
            flash("Please Login First", 'danger')
            return redirect(url_for('login'))



##################################################################
@app.route('/staff/deletedish/<dish_id>')
def deletedish(dish_id):
    if 'username' in session:
        dish = Dish.query.filter_by(id = dish_id).first()
        db.session.delete(dish)
        db.session.commit()

        flash('Dish {} has been deleted'.format(dish.name))
        return redirect(url_for('menu'))
    
    else:
        flash("Please Login First")
        return redirect(url_for('login'))


##################################################################
@app.route('/menu')
def menu():
    dishes = Dish.query.order_by(Dish.cat_id).all()
    categories = Category.query.order_by(Category.id).all()

    if 'username' in session:
        return render_template('menu.html', categories = categories, dishes = dishes, 
                                page_title = 'Menu', username = session['username'])

    return render_template('menu.html', categories = categories, 
                            dishes = dishes, page_title = 'Menu')


##################################################################
@app.route('/history')
def history():
    if 'username' in session:
        return render_template('information.html', page_title = 'About Page', 
                                username=session['username'])

    return render_template('information.html', page_title = 'About Page')