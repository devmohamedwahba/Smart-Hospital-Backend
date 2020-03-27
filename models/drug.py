from db import db
import datetime


class RecipeDrugAssos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    dose = db.Column(db.Integer)
    unit = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    rotes = db.Column(db.String(200))
    drug = db.relationship("DrugModel")
    recipe = db.relationship("RecipeModel", back_populates="drugs")

    @classmethod
    def find_all_drugs(cls, drug_id):
        return cls.query.filter_by(drug_id=drug_id).all()

    def json(self):
        return {
            "id": self.id,
            "drug_id": self.drug_id,
            "dose": self.dose,
            "unit": self.unit,
            "duration": self.duration,
            "rotes": self.rotes,
            "drug_details": [DrugModel.find_by_id(self.drug_id).json() if self.drug_id else ""]
        }


class DrugModel(db.Model):
    __tablename__ = "drugs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    unit = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expire_date = db.Column(db.String(200))

    # drug_details = db.relationship("RecipeDrugAssos", back_populates="drug")

    def __repr__(self):
        return f"this is {self.name}"

    def __init__(self, name, quantity, expire_date, unit):
        self.name = name
        self.quantity = quantity
        self.expire_date = expire_date
        self.unit = unit

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "created_at": str(self.created_at),
            "expire_date": str(self.expire_date),
            "unit": self.unit,
            "role_id": [role.name for role in DrugModel.find_by_id(self.id).roles]
        }

    @classmethod
    def find_all_drugs(cls):
        return cls.query.order_by(DrugModel.id.desc()).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
