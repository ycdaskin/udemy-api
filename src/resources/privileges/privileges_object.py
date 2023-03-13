from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.privileges.privileges_crud import *
from src.auth.auth import token_required


class PrivilegeCollection(Resource):

    @token_required
    def get(self):
        try:
            data = get_privileges()
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
            id = create_privilege(data)
            return make_response(jsonify(
                status="ok",
                msg="Privilege created successfully",
                privilege_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class PrivilegeItem(Resource):
    @token_required
    def get(self, id):
        try:
            data = get_privileges(id=id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


    @token_required
    def patch(self, id):
        try:
            data = request.get_json(force=True)
            update_privilege(data, id)
            return make_response(jsonify(
                status="ok",
                msg="Privilege updated successfully",
                privilege_id=id
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)

    @token_required
    def delete(self, id):
        try:
            delete_privilege(id)
            return make_response(jsonify(
                status="ok",
                msg="Privilege deleted successfully",
                privilege_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)

