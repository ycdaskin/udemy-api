from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.phone_validation.phone_validation_crud import *


class PhoneValidation(Resource):

    def post(self):
        try:
            auth = request.headers["Authorization"]
            token = auth.split(" ")[1]
            if token != "BUjX?rW!FX$TRA3a5n7+umd!2c&&^-SPFK7ERUrRRF#NMBJDWPk?HGySsCXM@vPC":
                return make_response(jsonify(
                    msg="Not authorized",
                    status="fail"
                ), 401)
            data = request.get_json(force=True)
            user_id = validate_phone_number(data)
            if user_id is None:
                return make_response(jsonify(
                    status="fail",
                    msg="No data found",
                    user_id=None
                ), 412)
            return make_response(jsonify(
                status="success",
                msg="Phone number is valid",
                user_id=user_id
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                msg=ex.args[0],
                status="fail"
            ), 500)


