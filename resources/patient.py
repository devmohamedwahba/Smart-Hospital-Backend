from flask_restful import Resource, reqparse
from models.patient import PatientModel
from models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.patient import UserPatientRecipeAssos
from db import db


class PatientSearchById(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "id", type=str, required=True, help="this field is required"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        patient = PatientModel.find_by_id(_id=data['id'])
        if not patient:
            return {"message": "No Patient Fount"}, 400
        return patient.json(), 200


class PatientSearchByNationalId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "national_id", type=str, required=True, help="this field is required"
    )

    @classmethod
    @jwt_required
    def post(cls):
        data = cls.parser.parse_args()
        patient = PatientModel.find_by_national_id(data.national_id)
        if not patient:
            return {"message": "No Patient Fount"}, 400
        return patient.json(), 200


class Patient(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "national_id", type=str, required=True, help="this field is required"
    )

    parser.add_argument(
        "nationality", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "mobile", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "age", type=int, required=True, help="this field is required"
    )
    parser.add_argument(
        "diagnostic", type=str, required=True, help="this field is required"
    )

    @classmethod
    @jwt_required
    def post(cls):
        data = cls.parser.parse_args()
        if PatientModel.find_by_mobile(data.mobile):
            return {"message": "this mobile already Exist"}, 404
        if PatientModel.find_by_national_id(data.national_id):
            return {"message": "Patient with this national id already exist"}, 404
        patient = PatientModel(**data)
        patient.save_to_db()

        current_user_id = get_jwt_identity()
        user_patient_recipe = UserPatientRecipeAssos(user_id=current_user_id, patient_id=patient.id)
        db.session.add(user_patient_recipe)
        db.session.commit()
        return {"message": "patient Created Successfully"}, 201


class Patients(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        patients = PatientModel.find_all_patients()
        if not patients:
            return {"message": "there is no patients"}
        return [patient.json() for patient in patients]
