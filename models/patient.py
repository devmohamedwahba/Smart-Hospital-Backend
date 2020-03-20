from db import db
import datetime
from models.department import DepartmentModel
from models.recipe import RecipeModel
from models.recipe import RecipeModel



class UserPatientRecipeAssos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    user = db.relationship("UserModel")
    patient = db.relationship("PatientModel", back_populates="users")
    recipe = db.relationship("RecipeModel")

    def json(self):
        return {
            "doctor_id": self.user_id,
            "recipe_id": self.recipe_id if self.recipe_id else ''
        }

    @classmethod
    def find_by_patient_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id).first()


class PatientModel(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    national_id = db.Column(db.String(80), unique=True)
    nationality = db.Column(db.String(200))
    mobile = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer)
    diagnostic = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    users = db.relationship("UserPatientRecipeAssos",
                            back_populates="patient")

    # patient_recipe = db.relationship("RecipeModel",
    #                                  backref="recipe")

    def __repr__(self):
        return f"this is {self.name}"

    def __init__(self, name, national_id, nationality, mobile, age, diagnostic):

        self.name = name
        self.national_id = national_id
        self.nationality = nationality
        self.mobile = mobile
        self.age = age
        self.diagnostic = diagnostic

    def json(self):
        return {
            "id":self.id,
            "name": self.name,
            "national_id": self.national_id,
            "nationality": self.nationality,
            "mobile": self.mobile,
            "age": self.age,
            "diagnostic": self.diagnostic,
            "patient_details": [doctor.json() for doctor in PatientModel.find_by_id(self.id).users]
        }

    @classmethod
    def find_all_patients(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_national_id(cls, national_id):
        return cls.query.filter_by(national_id=national_id).first()

    @classmethod
    def find_by_mobile(cls, mobile):
        return cls.query.filter_by(mobile=mobile).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

