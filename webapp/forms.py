from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from webapp.models import Dish, Category


categories = Category.query.all()
cat_choice = []
for cat in categories:
    cat_choice.append((cat.id, cat.cat_name))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddDish(FlaskForm):
    name = StringField('Dish Name', validators=[DataRequired()])
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    image = FileField('Image for the Dish',validators=[ FileAllowed(['jpg','png'])])
    cat_name = SelectField('Category Name', choices = cat_choice, coerce = int)
    submit = SubmitField('Add')

class EditDish(FlaskForm):
    name = StringField('Dish Name', validators=[DataRequired()])
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    image = FileField('Image for the Dish', validators=[FileAllowed(['jpg','png'])])
    cat_name = SelectField('Category Name', choices = cat_choice, coerce = int)
    submit = SubmitField('Update')

class EditCategory(FlaskForm):
    cat_name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddCategory(FlaskForm):
    name = TextAreaField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add')
