from flask import make_response, jsonify, request
from flask_restful import Resource
from src.auth.auth import refresh_token_required, get_identity, create_token, create_refresh_token, \
    update_session_by_refresh_token


class RefreshToken(Resource):

    @refresh_token_required
    def post(self):
        try:
            auth = request.headers.get("Authorization")
            refresh_token = auth.split(" ")[1]
            identity = get_identity(refresh_token)
            access_token = create_token(identity=identity)
            update_session_by_refresh_token(access_token, refresh_token)
            #refresh_token = create_refresh_token(identity=identity, related_token=access_token)
            return make_response(jsonify(
                token=access_token,
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)
