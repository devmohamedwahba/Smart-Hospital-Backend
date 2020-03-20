from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, UserLogout, Users
from resources.role import UserRole, UserRoles
from resources.drug import Drugs, Drug, RegisterDrug,DoctorDrug, DrugName
from resources.patient import PatientSearchById, Patient, Patients, PatientSearchByNationalId
from resources.recipe import Recipe, SearchRecipeById, RecipeSpend
from resources.department import Deprtment, Departments

app = Flask(__name__)
app.secret_key = "you will never gi ss password"
app.config.from_object("config")
CORS(app)
db = SQLAlchemy(app)

api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
            decrypted_token["jti"] in BLACKLIST
    )


"""  User Api """
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")

api.add_resource(Users, "/users")
api.add_resource(User, "/user/<int:user_id>")

"""        Roles Api             """
api.add_resource(UserRole, '/role')
api.add_resource(UserRoles, '/roles')

"""  Drugs """
api.add_resource(Drugs, '/drugs')
api.add_resource(RegisterDrug, '/drug')
api.add_resource(Drug, '/drug/<int:drug_id>')
api.add_resource(DrugName, '/drug/<string:drug_name>')
api.add_resource(DoctorDrug, '/doctor_drug')




""" search by id search national_id   add patient add recipe """
""" Doctor Api """
api.add_resource(PatientSearchById, '/search')
api.add_resource(PatientSearchByNationalId, '/search/national_id')
api.add_resource(Patient, '/patient')
api.add_resource(Patients, '/patients')

api.add_resource(Deprtment, '/department')
api.add_resource(Departments, '/departments')

api.add_resource(Recipe, '/recipe')
api.add_resource(SearchRecipeById, '/recipe/search/<int:id>')
api.add_resource(RecipeSpend, '/recipe_spend')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
