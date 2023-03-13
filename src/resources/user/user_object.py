from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.user.user_crud import *
from src.auth.auth import token_required


class UserCollection(Resource):

    @token_required
    def get(self):
        try:
            data = get_users()
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
            id = create_user(data)
            return make_response(jsonify(
                status="ok",
                msg="User created successfully",
                user_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)



class UserItem(Resource):
    @token_required
    def get(self, id):
        try:
            data = get_users(id=id)
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
            update_user(data, id)
            return make_response(jsonify(
                status="ok",
                msg="User updated successfully",
                user_id=id
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)

    @token_required
    def delete(self, id):
        try:
            delete_user(id)
            return make_response(jsonify(
                status="ok",
                msg="User deleted successfully",
                user_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


class UserBatch(Resource):

    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            ids = data["user_ids"]
            delete_users(ids)
            return make_response(jsonify(
                status="ok",
                msg="Users deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class UserDetails(Resource):

    @token_required
    def get(self, id):
        try:
            data = get_user_details(id=id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)
