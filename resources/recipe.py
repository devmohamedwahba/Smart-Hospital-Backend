from flask_restful import Resource, reqparse
from models.recipe import RecipeModel, RecipeSpendAssos
from models.drug import DrugModel, RecipeDrugAssos
from models.patient import UserPatientRecipeAssos
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import math


class Recipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "title", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "end_date", type=str, required=True, help="this field is required"
    )
    parser.add_argument(
        "notes", type=str, required=True, help="this field is required"
    )
    # parser.add_argument(
    #     "dept_id", type=int, required=True, help="this field is required"
    # )
    parser.add_argument(
        "patient_id", type=int, required=True, help="this field is required"
    )
    parser.add_argument(
        "drugs",
        action='append',
    )

    @classmethod
    @jwt_required
    def post(cls):
        data = cls.parser.parse_args()
        drugs = []
        for item in data.drugs:
            x = item.replace("'", '"')
            var = json.loads(x)
            drug_id = var['drug_id']
            drug = RecipeDrugAssos(drug_id=drug_id, dose=var['dose'], unit=var['unit'], duration=var['duration'],
                                   rotes=var['rotes'])
            drugs.append(drug)

        recipe = RecipeModel(title=data.title, end_date=data.end_date, notes=data.notes,
                             drugs=drugs)

        recipe.save_to_db()
        current_user_id = get_jwt_identity()
        recipe = recipe.id
        patient = data.patient_id
        user_patient_recipe = UserPatientRecipeAssos(user_id=current_user_id, patient_id=patient, recipe_id=recipe)
        user_patient_recipe.save_to_db()

        return {"message": "Recipe created successfully"}


class SearchRecipeById(Resource):
    @classmethod
    def get(cls, id):
        recipe = RecipeModel.find_by_id(_id=id)
        if not recipe:
            return {"message": "No recipe Fount"}, 400
        return recipe.json(), 200


class RecipeSpend(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "recipe_id", type=int, required=True, help="this field is required"
    )
    parser.add_argument(
        "drugs",
        action='append',
    )

    @classmethod
    @jwt_required
    def post(cls):
        data = cls.parser.parse_args()
        details = []
        for item in data.drugs:
            x = item.replace("'", '"')
            var = json.loads(x)
            drug_id = var['drug_id']
            drug = DrugModel.find_by_id(drug_id)

            discount = (var['dose'] * var['duration'] * var['unit']) / (drug.unit)
            information = {
                "drug_name": drug.name,
                "quantity": math.ceil(discount)
            }
            details.append(information)
            db.session.commit()

            if (drug.quantity - discount) > 0:
                current_user_id = get_jwt_identity()
                spend_recipe = RecipeSpendAssos(user_id=current_user_id, recipe_id=data.recipe_id)
                db.session.add(spend_recipe)
                db.session.commit()
                drug.quantity = (drug.quantity - math.ceil((discount)))
                db.session.commit()


            else:
                stockDrugs = []
                stockDrugs.append(drug)
                return {
                           "message": "Not enough quantity of this drug",
                           "data": [],
                           "drug": [drug.json() for drug in stockDrugs]

                       }, 404
        return {"message": "Recipe Spend successful",
                "data": details
                }
