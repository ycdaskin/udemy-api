from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.user_privileges.user_privileges_crud import *
from src.auth.auth import token_required


class UserPrivilegeCollection(Resource):
    @token_required
    def get(self):
        try:
            data = get_user_privileges()
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
            id = create_user_privilege(data)
            return make_response(jsonify(
                status="ok",
                msg="User privilege created successfully",
                privilege_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class UserPrivilegeItem(Resource):
    @token_required
    def get(self, id):
        try:
            data = get_user_privileges(id=id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

    @token_required
    def delete(self, id):
        try:
            delete_user_privilege(id)
            return make_response(jsonify(
                status="ok",
                msg="User privilege deleted successfully",
                privilege_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)

