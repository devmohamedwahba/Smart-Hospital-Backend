from flask_restful import Resource, reqparse
from models.drug import DrugModel, RecipeDrugAssos
from models.role import RoleModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import UserModel
from db import db


class Drugs(Resource):
    def get(self):
        drugs = DrugModel.find_all_drugs()
        if not drugs:
            return {"message": "There is no drugs in database"}, 404
        return [drug.json() for drug in drugs], 200


class Drug(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "quantity", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "expire_date", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "unit", type=int, required=True, help="this field is required"
    )
    parser.add_argument(
        "role_id", type=int, required=True, help="this field is required"
    )

    @classmethod
    def get(cls, drug_id: int):
        drug = DrugModel.find_by_id(drug_id)
        if not drug:
            return {"message": "Drug Not Found"}, 404
        return drug.json(), 200

    @classmethod
    @jwt_required
    def delete(cls, drug_id: int):
        drug = DrugModel.find_by_id(drug_id)

        if not drug:
            return {"message": "Drug NOT FOUND"}, 404
        all_drugs = RecipeDrugAssos.find_all_drugs(drug_id)
        for drug_id_delete in all_drugs:
            drug_id_delete.drug_id = None
            db.session.commit()

        drug.delete_from_db()
        return {"message": "Drug Deleted Successfully"}, 200

    @classmethod
    def put(cls, drug_id: int):
        drug = DrugModel.find_by_id(drug_id)
        if not drug:
            return {"message": "Drug Not Found"}, 404

        data = cls.parser.parse_args()
        drug.name = data['name']
        drug.quantity = data['quantity']
        drug.expire_date = data['expire_date']
        drug.unit = data['unit']
        drug.role_id = data['role_id']

        role = RoleModel.find_by_id(data.role_id)
        drug.roles = []
        drug.roles.append(role)
        db.session.commit()
        return {"message": "Drug Updated Successfully"}


class DrugName(Resource):
    @classmethod
    def get(cls, drug_name):
        drug = DrugModel.find_by_name(drug_name)
        if not drug:
            return {"message": "Drug Not Found"}, 404
        return drug.json(), 200


class RegisterDrug(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "quantity", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "expire_date", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "unit", type=int, required=True, help="this field is required"
    )
    parser.add_argument(
        "role_id", type=int, required=True, help="this field is required"
    )

    @classmethod
    @jwt_required
    def post(cls):
        data = cls.parser.parse_args()
        drug = DrugModel(name=data.name, quantity=data.quantity, expire_date=data.expire_date, unit=data.unit)
        role = RoleModel.find_by_id(data.role_id)
        drug.roles.append(role)
        drug.save_to_db()
        return {"message": "Drug Created Successfully"}, 201


class DoctorDrug(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        current_user_id = get_jwt_identity()
        user = UserModel.find_by_id(current_user_id)
        role = RoleModel.find_by_id(user.role_id)
        drugs = role.drugs
        if not drugs:
            return {"message": "There is no Drugs in database"}, 404
        return [drug.json() for drug in drugs], 200
