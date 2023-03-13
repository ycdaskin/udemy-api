from flask import Flask, jsonify, make_response
from src.resources.car.car_object import CarCollection, CarItem
from src.resources.privileges.privileges_object import PrivilegeCollection, PrivilegeItem
from src.resources.company.company_object import CompanyCollection, CompanyItem, CompanyBatch, CompanyDetails
from src.resources.user_privileges.user_privileges_object import UserPrivilegeCollection, UserPrivilegeItem
from src.resources.user.user_object import UserCollection, UserItem, UserBatch, UserDetails
from src.resources.token.token_object import Token, Logout
from src.resources.refresh_token.refresh_token_object import RefreshToken
from src.resources.phone_validation.phone_validation_object import PhoneValidation
from src.resources.password_reset.password_reset_object import PasswordReset, VerificationCode
from src.resources.user_role.user_role_object import UserRoleItem, UserRoleCollection, UserRoleBatch
from src.resources.role_privilege.role_privilege_object import RolePrivilegeCollection
from src.resources.user_role_rel.user_role_rel_object import UserRoleRelCollection, UserRoleRelDetails, UserRoleRelBatch
from src.s3_storage.s3_object import S3
from src.resources.building.building_object import BuildingCollection, BuildingBatch, BuildingItem
from src.resources.gate.gate_object import GateItem, GateCollection, GateBatch, GateDetails
from src.resources.access_point.access_point_object import AccessPointBatch, AccessPointItem, AccessPointCollection
from src.resources.user_access_privilege.user_access_privilege_object import UserAccessCollection, UserAccessByGate, UserAccessByGateBatch

from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)


api.add_resource(Token, '/api/login')
api.add_resource(RefreshToken, '/api/refresh_token')
api.add_resource(Logout, '/api/logout')

api.add_resource(CarCollection, "/api/cars")
api.add_resource(CarItem, "/api/cars/<id>")

api.add_resource(PrivilegeCollection, "/api/privileges")
api.add_resource(PrivilegeItem, "/api/privileges/<id>")

api.add_resource(CompanyCollection, "/api/companies")
api.add_resource(CompanyItem, "/api/companies/<id>")
api.add_resource(CompanyBatch, "/api/companies")
api.add_resource(CompanyDetails, "/api/companies/details/<id>")

api.add_resource(UserPrivilegeCollection, "/api/user_privileges")
api.add_resource(UserPrivilegeItem, "/api/user_privileges/<id>")

api.add_resource(UserCollection, "/api/users")
api.add_resource(UserBatch, "/api/users")
api.add_resource(UserItem, "/api/users/<id>")
api.add_resource(UserDetails, "/api/users/details/<id>")

api.add_resource(UserRoleCollection, "/api/user_roles")
api.add_resource(UserRoleItem, "/api/user_roles/<id>")
api.add_resource(UserRoleBatch, "/api/user_roles")

api.add_resource(PhoneValidation, "/api/validate_phone")
api.add_resource(PasswordReset, "/api/reset_password")
api.add_resource(VerificationCode, "/api/validate_otp")

api.add_resource(BuildingItem, "/api/buildings/<id>")
api.add_resource(BuildingCollection, "/api/buildings")
api.add_resource(BuildingBatch, "/api/buildings")

api.add_resource(GateItem, "/api/gates/<id>")
api.add_resource(GateCollection, "/api/gates")
api.add_resource(GateBatch, "/api/gates")
api.add_resource(GateDetails, "/api/gates/details/<id>")

api.add_resource(AccessPointItem, "/api/access_points/<id>")
api.add_resource(AccessPointCollection, "/api/access_points")
api.add_resource(AccessPointBatch, "/api/access_points")

api.add_resource(RolePrivilegeCollection, '/api/role_privileges')

api.add_resource(UserRoleRelCollection, '/api/user_role_rel')
api.add_resource(UserRoleRelDetails, '/api/user_role_rel/details')
api.add_resource(UserRoleRelBatch, '/api/user_role_rel/batch')

api.add_resource(UserAccessCollection, "/api/access_privs")
api.add_resource(UserAccessByGate, "/api/gate_privs")
api.add_resource(UserAccessByGateBatch, "/api/gate_privs/batch")


api.add_resource(S3, "/api/upload_file")

@app.route('/api/test')
def test():
    return make_response(jsonify(
        data={
            "message": "First trial with Flask on Heroku",
            "deployed_by": "Cagri Daskin",
            "status": "200 OK"
        }
    ), 200)


if __name__ == "__main__":
    #initialize()
    #initialize_auth_db()
    app.run(threaded=True, port=5001)

