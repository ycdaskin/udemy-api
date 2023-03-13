from flask import make_response, jsonify, request
from flask_restful import Resource
from src.resources.company.company_crud import *
from src.auth.auth import token_required


class CompanyCollection(Resource):
    @token_required
    def get(self):
        try:
            data = get_companies()
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
            id = create_company(data)
            return make_response(jsonify(
                status="ok",
                msg="company created successfully",
                company_id=id
            ), 201)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class CompanyItem(Resource):
    @token_required
    def get(self, id):
        try:
            data = get_companies(id=id)
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
            update_company(data, id)
            return make_response(jsonify(
                status="ok",
                msg="Company updated successfully",
                company_id=id
            ), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)

    @token_required
    def delete(self, id):
        try:
            delete_company(id)
            return make_response(jsonify(
                status="ok",
                msg="Company deleted successfully",
                company_id=id
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=ex.args[0]
            ), 500)


class CompanyBatch(Resource):

    @token_required
    def delete(self):
        try:
            data = request.get_json(force=True)
            ids = data["company_ids"]
            delete_companies(ids)
            return make_response(jsonify(
                status="ok",
                msg="Companies deleted successfully"
            ), 204)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)


class CompanyDetails(Resource):

    @token_required
    def get(self, id):
        try:
            data = get_company_details(id=id)
            return make_response(jsonify(data=data), 200)
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=str(ex.args[0])
            ), 500)
