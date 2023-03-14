from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.access_control.user_activity.user_activity_crud import *
from src.auth.auth import token_required


class UserActivityCollection(Resource):

    @token_required
    def get(self):
        try:
            data = get_user_activities()
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
            id = create_user_activity(data)
            return make_response(jsonify(
                status="ok",
                msg="User activity created successfully",
                record_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)



class UserActivityItem(Resource):

    @token_required
    def get(self, id):
        try:
            data = get_user_activities(id=id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)




    @token_required
    def delete(self, id):
        try:
            delete_user_activity(id)
            return make_response(jsonify(
                status="ok",
                msg="User activity deleted successfully",
                record_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


class UserActivityBatch(Resource):
    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            ids = data["user_activity_ids"]
            delete_user_activities(ids)
            return make_response(jsonify(
                status="ok",
                msg="User activities deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class UserActivityByUser(Resource):
    @token_required
    def get(self, user_id):
        try:
            data = get_user_activities_by_user(user_id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)
