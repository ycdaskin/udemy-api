from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.gate.gate_crud import *
from src.auth.auth import token_required


class GateCollection(Resource):

    @token_required
    def get(self):
        try:
            data = get_gates()
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
            id = create_gate(data)
            return make_response(jsonify(
                status="ok",
                msg="Gate created successfully",
                building_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)



class GateItem(Resource):

    @token_required
    def get(self, id):
        try:
            data = get_gates(id=id)
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
            update_gate(data, id)
            return make_response(jsonify(
                status="ok",
                msg="Gate updated successfully",
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
            delete_gate(id)
            return make_response(jsonify(
                status="ok",
                msg="Gate deleted successfully",
                gate_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


class GateBatch(Resource):
    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            ids = data["gate_ids"]
            delete_gates(ids)
            return make_response(jsonify(
                status="ok",
                msg="Gates deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

class GateDetails(Resource):
    @token_required
    def get(self, id):
        try:
            data = get_gate_details(id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)
