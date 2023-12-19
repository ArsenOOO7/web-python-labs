from marshmallow import fields, validate, validates_schema, ValidationError

from app import ma
from app.domain.HouseholdAppliance import HouseholdAppliance, HouseholdApplianceType


class HouseholdApplianceResponseDto(ma.SQLAlchemySchema):
    class Meta:
        model = HouseholdAppliance
        load_instance = True

    id = fields.Integer(required=False)
    type = fields.String(required=True)
    name = fields.String(required=True, validate=[validate.Length(min=3, max=40)])
    brand = fields.String(required=True, validate=[validate.Length(max=40)])
    price = fields.Float(required=True, validate=[validate.Range(min=1.0)])
    purchased_at = fields.String(required=False)

    @validates_schema
    def validate_type(self, data, **kwargs):
        hha_type = data.get('type')
        types = [type.value for type in HouseholdApplianceType]
        if hha_type not in types:
            raise ValidationError(f"Undefined type {hha_type}")

    @validates_schema
    def validate_name(self, data, **kwargs):
        name = data.get('name')
        id = data.get('id')
        household_appliance = HouseholdAppliance.query.filter(HouseholdAppliance.name == name).first()
        if household_appliance and household_appliance.id != id:
            raise ValidationError('Household appliance with this name is already exists.')
