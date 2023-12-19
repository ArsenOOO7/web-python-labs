from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from app.api.household_appliances_rest.controller import HouseholdApplianceListRestController, \
    HouseholdApplianceRestController

household_appliances_bp = Blueprint("household_appliances_rest", __name__)
api = Api(household_appliances_bp, errors=household_appliances_bp.app_errorhandler)

api.add_resource(HouseholdApplianceListRestController, '/list')
api.add_resource(HouseholdApplianceRestController, '/<int:id>', '/', '')


@household_appliances_bp.app_errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
