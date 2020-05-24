from webapp import db

#create table 'Category': 
class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cat_name = db.Column(db.String(),unique = True, nullable = False)
    dish = db.relationship('Dish', backref = 'category', lazy = True)

    def __repr__(self):
        return f"Categeory: '{self.cat_name}'"

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    ingredient = db.Column(db.String(), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    image = db.Column(db.String(), nullable = False)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)

    def __repr__(self):
        return f"Dish('{self.name}', '{self.ingredient}', '{self.price}' , '{self.cat_id}')"

