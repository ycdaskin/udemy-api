from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.access_point.access_point_crud import *
from src.auth.auth import token_required



class AccessPointCollection(Resource):

    @token_required
    def get(self):
        try:
            data = get_access_points()
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
            id = create_access_point(data)
            return make_response(jsonify(
                status="ok",
                msg="Access point created successfully",
                access_point_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


class AccessPointItem(Resource):
    @token_required
    def get(self, id):
        try:
            data = get_access_points(id=id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


    @token_required
    def patch(self):
        try:
            data = request.get_json(force=True)
            update_access_point(data, id)
            return make_response(jsonify(
                status="ok",
                msg="Access point updated successfully",
                access_point_id=id
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)

    @token_required
    def delete(self, id):
        try:
            delete_access_point(id)
            return make_response(jsonify(
                status="ok",
                msg="Access point deleted successfully",
                access_point_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


class AccessPointBatch(Resource):
    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            ids = data["access_point_ids"]
            delete_access_points(ids)
            return make_response(jsonify(
                status="ok",
                msg="Access points deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)