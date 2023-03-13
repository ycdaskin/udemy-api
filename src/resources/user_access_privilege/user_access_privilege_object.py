from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.user_access_privilege.user_access_privilege_crud import *
from src.auth.auth import token_required


class UserAccessCollection(Resource):
    @token_required
    def get(self):
        try:
            incoming = None
            try:
                incoming = request.get_json(force=True)
            except:
                pass
            user_id = incoming["user_id"] if incoming is not None else None
            data = get_user_access_privs() if user_id is None else get_aceess_privs_by_user(user_id)
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
            create_user_access_privs(data)
            return make_response(jsonify(
                status="ok",
                msg="User access privilege created successfully",
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

    @token_required
    def delete(self):
        try:
            incoming = request.get_json(force=True)
            user_id = incoming["user_id"]
            delete_access_privs_of_user(user_id=user_id)
            return make_response(jsonify(
                status="ok",
                msg="User access privileges deleted successfully",
                user_id=user_id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)



class UserAccessByGate(Resource):
    @token_required
    def get(self):
        try:
            incoming = request.get_json(force=True)
            user_id = incoming["user_id"]
            gate_id = incoming["gate_id"]
            data = get_user_access_privs_by_gate(user_id, gate_id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


    @token_required
    def put(self):
        try:
            incoming = request.get_json(force=True)
            user_id = incoming["user_id"]
            gate_id = incoming["gate_id"]
            grant_user_access_privs_by_gate(user_id, gate_id)
            return make_response(jsonify(
                status="ok",
                msg="User access privileges granted successfully",
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

    @token_required
    def delete(self):
        try:
            incoming = request.get_json(force=True)
            user_id = incoming["user_id"]
            gate_id = incoming["gate_id"]
            revoke_user_access_privs_by_gate(user_id, gate_id)
            return make_response(jsonify(
                status="ok",
                msg="User access privileges revoked successfully",
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class UserAccessByGateBatch(Resource):
    @token_required
    def delete(self):
        try:
            incoming = request.get_json(force=True)
            revoke_user_access_privs_by_gate_multiple(incoming["data"])
            return make_response(jsonify(
                status="ok",
                msg="User access privileges revoked successfully",
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


