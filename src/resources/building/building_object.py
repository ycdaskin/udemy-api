from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.building.building_crud import *
from src.auth.auth import token_required



class BuildingCollection(Resource):

    @token_required
    def get(self):
        try:
            data = get_buildings()
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
            id = create_building(data)
            return make_response(jsonify(
                status="ok",
                msg="Building created successfully",
                building_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class BuildingItem(Resource):
    @token_required
    def get(self, id):
        try:
            data = get_buildings(id=id)
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
            update_building(data, id)
            return make_response(jsonify(
                status="ok",
                msg="Building updated successfully",
                building_id=id
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)

    @token_required
    def delete(self, id):
        try:
            delete_building(id)
            return make_response(jsonify(
                status="ok",
                msg="Building deleted successfully",
                building_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


class BuildingBatch(Resource):
    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            ids = data["building_ids"]
            delete_buildings(ids)
            return make_response(jsonify(
                status="ok",
                msg="Buildings deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)