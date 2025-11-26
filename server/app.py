#!/usr/bin/env python3
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
import os

from models import db
from routes import Restaurants, RestaurantByID, Pizzas, RestaurantPizzas

# ------------------ CONFIG ----------------------

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

# ------------------ ROUTES ----------------------

@app.route("/")
def index():
    return "<h1>Code Challenge</h1>"

# flask-restful resources
api.add_resource(Restaurants, "/restaurants")
api.add_resource(RestaurantByID, "/restaurants/<int:id>")
api.add_resource(Pizzas, "/pizzas")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")


# ------------------ MAIN ------------------------

if __name__ == "__main__":
    app.run(port=5555, debug=True)
