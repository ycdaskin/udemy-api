from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.car.car_crud import *
from src.auth.auth import token_required

class CarCollection(Resource):
    @token_required
    def get(self):
        try:
            data = get_cars()
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

    @token_required
    def put(self):
        try:
            data = request.get_json(force=True)
            car_id = create_car(data)
            return make_response(jsonify(
                status="ok",
                msg="car created successfully",
                car_id=car_id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class CarItem(Resource):
    @token_required
    def get(self, car_id):
        try:

            cars = get_cars(car_id=car_id)
            return make_response(jsonify(cars=cars), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

    @token_required
    def patch(self, car_id):
        try:
            data = request.get_json(force=True)
            update_car(data, car_id)
            return make_response(jsonify(
                status="ok",
                msg="car updated successfully",
                car_id=car_id
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


    @token_required
    def delete(self, car_id):
        try:
            delete_car(car_id)
            return make_response(jsonify(
                status="ok",
                msg="car deleted successfully",
                car_id=car_id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)

