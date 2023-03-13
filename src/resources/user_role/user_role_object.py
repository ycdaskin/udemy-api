from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.user_role.user_role_crud import *
from src.auth.auth import token_required


class UserRoleCollection(Resource):

    @token_required
    def get(self):
        try:
            company = None
            try:
                incoming = request.get_json(force=True)
                company = incoming["company"] if "company" in incoming else None
            except:
                pass
            data = get_user_roles_by_company(company_id=company)
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
            id = create_user_role(data)
            return make_response(jsonify(
                status="ok",
                msg="User role created successfully",
                user_role_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class UserRoleItem(Resource):
    @token_required
    def get(self, id):
        try:
            data = get_user_role(id=id)
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
            update_user_role(data, id)
            return make_response(jsonify(
                status="ok",
                msg="User role updated successfully",
                user_role_id=id
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


    @token_required
    def delete(self, id):
        try:
            delete_user_role(id)
            return make_response(jsonify(
                status="ok",
                msg="User role deleted successfully",
                user_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


class UserRoleBatch(Resource):

    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            ids = data["role_ids"]
            delete_user_roles(ids)
            return make_response(jsonify(
                status="ok",
                msg="User roles deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)
