from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from models.user import UserModel
from models.recipe import RecipeSpendAssos
from models.patient import UserPatientRecipeAssos
from blacklist import BLACKLIST
from werkzeug.security import generate_password_hash, check_password_hash
from db import db

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "email", type=str, required=True, help="this field is required"
)
_user_parser.add_argument(
    "password", type=str, required=True, help="password cant be blank"
)


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="userName cant be blank"
    )
    parser.add_argument(
        "email", type=str, required=True, help="email is required"
    )
    parser.add_argument(
        "password", type=str, required=True, help="password can not be blank"
    )
    parser.add_argument(
        "role_id", type=int, required=True, help="role_id field can not be blank"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        if UserModel.find_by_email(data["email"]):
            return {"message": "User Already Exist"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User Created Successfully"}, 201


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="userName cant be blank"
    )
    parser.add_argument(
        "email", type=str, required=True, help="email is required"
    )
    parser.add_argument(
        "password", type=str, required=True, help="password can not be blank"
    )
    parser.add_argument(
        "role_id", type=int, required=True, help="role_id field can not be blank"
    )

    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User Not Found"}, 404
        return user.json(), 200

    @classmethod
    def put(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User Not Found"}, 404

        data = User.parser.parse_args()

        user.username = data['username']
        user.email = data['email']
        user.password = generate_password_hash(data['password'])
        user.role_id = data['role_id']
        user.save_to_db()
        return {"message": "User Updated Successfully"}

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "USER NOT FOUND"}, 404
        recipe_of_user = RecipeSpendAssos.delete_user_recipe(user_id)
        for delete_user in recipe_of_user:
            delete_user.user_id = None
            db.session.commit()
        recipe_of_user_patient = UserPatientRecipeAssos.delete_user_recipe(user_id)
        for delete_user in recipe_of_user_patient:
            delete_user.user_id = None
            db.session.commit()

        user.delete_from_db()
        return {"message": "User Deleted Successfully"}, 200


class Users(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        users = UserModel.find_all_users()
        if not users:
            return {"message": "There is no User in database"}, 404
        return [user.json() for user in users], 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token,
                       "role": user.role.json()
                   }, 200

        return {"message": "Email Or Password Invalid"}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "User Logout Successfully".format(user_id)}, 200
