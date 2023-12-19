from flask import request
from flask_restful import Resource

from app import data_base, jwt_utils
from app.api.household_appliances_rest.schemas import HouseholdApplianceResponseDto
from app.domain.HouseholdAppliance import HouseholdAppliance
from app.util.exceptions import EntityNotFoundException


class HouseholdApplianceRestController(Resource):
    @jwt_utils.pre_authorize
    def get(self, id):
        return HouseholdApplianceResponseDto().dump(self.__get_existent(id)), 200

    @jwt_utils.pre_authorize
    def post(self):
        schema = HouseholdApplianceResponseDto()
        household_appliance = schema.load(request.json)
        data_base.session.add(household_appliance)
        data_base.session.commit()

        return schema.dump(household_appliance), 201

    @jwt_utils.pre_authorize
    def put(self, id):
        entity = self.__get_existent(id)
        schema = HouseholdApplianceResponseDto()
        schema.id = id
        entity = schema.load(request.json, instance=entity)

        data_base.session.commit()
        return schema.dump(entity), 200

    @jwt_utils.pre_authorize
    def delete(self, id):
        entity = self.__get_existent(id)
        data_base.session.delete(entity)
        data_base.session.commit()
        return 204

    def __get_existent(self, id):
        household_appliance = HouseholdAppliance.query.get(id)
        if not household_appliance:
            raise EntityNotFoundException('Household Appliance', id)

        return household_appliance


class HouseholdApplianceListRestController(Resource):

    @jwt_utils.pre_authorize
    def get(self):
        return HouseholdApplianceResponseDto(many=True).dump(HouseholdAppliance.query.all())
