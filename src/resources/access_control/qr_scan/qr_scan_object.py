from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.access_control.qr_scan.qr_scan_crud import *
from src.auth.auth import token_required


class QrScan(Resource):
    @token_required
    def post(self):
        try:
            data = request.get_json(force=True)
            scan_qr(data)
            return make_response(jsonify(
                status="ok",
                msg="Access success"
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


