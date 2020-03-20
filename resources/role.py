from flask_restful import Resource, reqparse
from models.role import RoleModel


class UserRole(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field is required"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = RoleModel(**data)
        if user.find_by_name(user.name):
            return {"message": "Role already Exists"}
        user.save_to_db()
        return {"message": "Role Created Successfully"}, 201


class UserRoles(Resource):
    @classmethod
    def get(cls):
        roles = RoleModel.find_all_roles()
        if not roles:
            return {"message": "There is no role in database"}, 404
        return [role.json() for role in roles], 200
