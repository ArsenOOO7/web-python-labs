from flask import request
from flask_restful import Resource

from app import data_base
from app.api.household_appliances_rest.schemas import HouseholdApplianceResponseDto
from app.domain.HouseholdAppliance import HouseholdAppliance
from app.util.exceptions import EntityNotFoundException


class HouseholdApplianceRestController(Resource):
    def get(self, id):
        return HouseholdApplianceResponseDto().dump(self.__get_existent(id))

    def post(self):
        schema = HouseholdApplianceResponseDto()
        household_appliance = schema.load(request.json)
        data_base.session.add(household_appliance)
        data_base.session.commit()

        return schema.dump(household_appliance)

    def put(self, id):
        entity = self.__get_existent(id)
        schema = HouseholdApplianceResponseDto()
        entity = schema.load(request.json, instance=entity)

        data_base.session.commit()
        return schema.dump(entity)

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

    def get(self):
        return HouseholdApplianceResponseDto(many=True).dump(HouseholdAppliance.query.all())
