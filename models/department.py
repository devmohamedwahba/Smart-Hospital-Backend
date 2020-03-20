from db import db


class DepartmentModel(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    max_quantity = db.Column(db.Integer)
    recipes = db.relationship('RecipeModel', lazy="dynamic")

    def __repr__(self):
        return f"this is {self.name}"

    def __init__(self, name, max_quantity):
        self.name = name
        self.max_quantity = max_quantity

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "max_quantity": self.max_quantity,
            # "recipes": [recipe.json() for recipe in self.recipes.all()]
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all_departments(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

