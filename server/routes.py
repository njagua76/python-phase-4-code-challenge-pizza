from flask import request, make_response, jsonify
from flask_restful import Resource
from models import db, Restaurant, Pizza, RestaurantPizza


# ------------------------ RESTAURANTS -----------------------------

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict(rules=("-restaurant_pizzas",)) for r in restaurants], 200


class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)

        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        return restaurant.to_dict(
            rules=("-restaurant_pizzas.restaurant",)
        ), 200

    def delete(self, id):
        restaurant = Restaurant.query.get(id)

        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        db.session.delete(restaurant)
        db.session.commit()

        return {}, 204


# --------------------------- PIZZAS -------------------------------

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict(rules=("-restaurant_pizzas",)) for p in pizzas], 200


# --------------------- RESTAURANT PIZZAS -------------------------

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_rp = RestaurantPizza(
                price=data.get("price"),
                pizza_id=data.get("pizza_id"),
                restaurant_id=data.get("restaurant_id")
            )

            db.session.add(new_rp)
            db.session.commit()

            response = new_rp.to_dict()
            response["pizza"] = new_rp.pizza.to_dict()
            response["restaurant"] = new_rp.restaurant.to_dict()

            return response, 201

        except ValueError:
            return {"errors": ["validation errors"]}, 400

