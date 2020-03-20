from db import db
from app import app
db.init_app(app=app)
from models.department import *
from models.role import *
from models.user import *
from models.drug import *
from models.patient import *
from models.recipe import *

db.create_all(app=app)
