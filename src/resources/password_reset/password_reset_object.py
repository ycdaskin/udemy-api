from flask import make_response, jsonify, request
from flask_restful import Resource
from src.auth.auth import get_user_by_secret_key, get_secret_key_by_verification_code, delete_verification_code
from src.resources.password_reset.password_reset_crud import update_password


class PasswordReset(Resource):

    def post(self):
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            if token != "BUjX?rW!FX$TRA3a5n7+umd!2c&&^-SPFK7ERUrRRF#NMBJDWPk?HGySsCXM@vPC":
                return make_response(jsonify(
                    msg="Not authorized",
                    status="fail"
                ), 401)
            verification_code = request.headers.get("Verification-Code")
            secret_key = request.headers.get("Secret-Key")
            user = get_user_by_secret_key(secret_key, verification_code)
            if user is None:
                return make_response(jsonify(
                    status="fail",
                    msg="Invalid or expired verification code"
                ), 404)
            data = request.get_json(force=True)
            password = data["password"]
            password_again = data["password_again"]
            if password != password_again or len(password) < 6:
                return make_response(jsonify(
                    msg="Password requirements not met",
                    status="fail"
                ), 404)
            update_password(user, password_again)
            delete_verification_code(secret_key)
            return make_response(jsonify(
                msg="Password reset successfully",
                status="success"
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                msg=ex.args[0],
                status="fail"
            ), 500)


class VerificationCode(Resource):

    def post(self):
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            if token != "BUjX?rW!FX$TRA3a5n7+umd!2c&&^-SPFK7ERUrRRF#NMBJDWPk?HGySsCXM@vPC":
                return make_response(jsonify(
                    msg="Not authorized",
                    status="fail"
                ), 401)
            verification_code = request.headers.get("Verification-Code")
            secret_key = get_secret_key_by_verification_code(verification_code)
            if secret_key is None:
                return make_response(jsonify(
                    status="fail",
                    msg="Invalid or expired verification code"
                ), 404)
            return make_response(jsonify(
                msg="Verification code is valid",
                status="success",
                secret_key=secret_key
            ))
        except Exception as ex:
            return make_response(jsonify(
                msg=ex.args[0],
                status="fail"
            ), 500)


