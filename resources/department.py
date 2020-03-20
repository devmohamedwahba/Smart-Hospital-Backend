from flask_restful import Resource, reqparse
from models.department import DepartmentModel
from flask_jwt_extended import jwt_required


class Deprtment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "max_quantity", type=int, required=True, help="this field is required"
    )

    @classmethod
    @jwt_required
    def post(cls):
        data = Deprtment.parser.parse_args()
        department = DepartmentModel(**data)
        department.save_to_db()
        return {"message": "department created"}, 200


class Departments(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        departments = DepartmentModel.find_all_departments()
        if not departments:
            return {"message": "There is No Departments"}
        return [department.json() for department in departments]
