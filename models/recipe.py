from db import db
import datetime


class RecipeSpendAssos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    user = db.relationship("UserModel")
    recipe = db.relationship("RecipeModel")

    @classmethod
    def delete_user_recipe(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()


class RecipeModel(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department = db.relationship('DepartmentModel')

    drugs = db.relationship("RecipeDrugAssos", back_populates="recipe")

    def __repr__(self):
        return f"this is {self.title}"

    # def __init__(self, title, end_date, notes, dept_id):
    #     self.title = title
    #     self.end_date = end_date
    #     self.notes = notes
    #     self.dept_id = dept_id

    def json(self):
        return {
            "id":self.id,
            "title": self.title,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "notes": self.notes,
            "dept_id": self.dept_id,
            "drugs": [drug.json() for drug in RecipeModel.find_by_id(self.id).drugs]
        }

    @classmethod
    def find_all_recipes(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

