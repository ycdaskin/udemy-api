from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.token.token_crud import *
from src.crypto.crypto import Crypto
from src.auth.auth import create_token, create_refresh_token, create_session, token_required, kill_session


class Token(Resource):

    @token_required
    def get(self):
        '''
        token'ın geçerli olup olmadığını kontrol etmek için kullanılır
        :return:
        '''
        try:
            return make_response(jsonify(
                status="success",
                msg="Valid token"
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)

    def post(self):
        try:
            data = request.get_json(force=True)
            user_name = data["user_name"]
            password = data["password"]
            cr = Crypto()
            enc_pass = cr.encrypt(password)
            user = get_user(user_name, enc_pass)
            if user is None:
                return make_response(jsonify(
                    status="Not authorized",
                    msg="Incorrect username and/or password"
                ), 401)
            privileges = get_user_privileges(user["id"])
            user['privileges'] = privileges
            token = create_token(identity=user["id"], company=user["company"])
            refresh_token = create_refresh_token(identity=user["id"], company=user["company"], related_token=token)
            create_session(user["id"], token, refresh_token)
            return make_response(jsonify(
                status="Authorized",
                user=user,
                token=token,
                refresh_token=refresh_token
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class Logout(Resource):

    def post(self):
        try:
            auth = request.headers["Authorization"]
            token = auth.split(" ")[1]
            kill_session(token)
            return make_response(jsonify(
                msg="Session killed successfully",
                status="success"
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)




