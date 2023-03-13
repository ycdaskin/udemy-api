from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.role_privilege.role_privilege_crud import *
from src.auth.auth import token_required


class RolePrivilegeCollection(Resource):

    @token_required
    def get(self):
        try:
            data = get_role_privileges()
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
            create_role_privilege(data)
            return make_response(jsonify(
                status="ok",
                msg="Role-privilege relation created"
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

    @token_required
    def patch(self):
        try:
            data = request.get_json(force=True)
            update_role_privilege(data)
            return make_response(jsonify(
                status="ok",
                msg="Role-privilege relation updated"
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


