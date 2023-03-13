from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.user_role_rel.user_role_rel_crud import *
from src.auth.auth import token_required


class UserRoleRelCollection(Resource):

    @token_required
    def put(self):
        try:
            data = request.get_json(force=True)
            create_user_role_rel(data)
            return make_response(jsonify(
                status="ok",
                msg="User-role relation created successfully"
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            delete_user_role_rel(data)
            return make_response(jsonify(
                status="ok",
                msg="User-role relation deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class UserRoleRelBatch(Resource):
    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            delete_user_role_rel_multiple(data["data"])
            return make_response(jsonify(
                status="ok",
                msg="User-role relations deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class UserRoleRelDetails(Resource):
    @token_required
    def get(self):
        try:
            data = get_user_role_rel_details()
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)
