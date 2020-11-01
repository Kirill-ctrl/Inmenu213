from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import Length

from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.adapters.enums.validation_errors import ValidationErrorEnum


def validate_phone_number(value: str):
    if len(value) != 11 or not value.isdigit():
        raise ValidationError([ErrorEnum.WRONG_PHONE_NUMBER_FORMAT])


class ContactsSchema(Schema):
    phone_number = fields.String(required=False, allow_none=True, validate=validate_phone_number)
    email = fields.Email(required=False, allow_none=True, validate=Length(max=50))
    site_link = fields.String(required=False, allow_none=True)
    facebook_link = fields.String(required=False, allow_none=True)
    instagram_link = fields.String(required=False, allow_none=True)
    vk_link = fields.String(required=False, allow_none=True)


class CoordsSchema(Schema):
    lat = fields.Integer(required=True, allow_none=False, error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    long = fields.Integer(required=True, allow_none=False, error_messages={'required': ValidationErrorEnum.NOT_FIELD})


class LocationSchema(Schema):
    full_address = fields.String(required=True, allow_none=False, error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    city = fields.String(required=True, allow_none=False, error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    country = fields.String(required=True, allow_none=False, error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    coords = fields.Dict(fields.String, required=True, allow_none=False, validate=lambda value: CoordsSchema().load(value), error_messages={'required': ValidationErrorEnum.NOT_FIELD})


class WeekDaySchema(Schema):
    is_holiday = fields.Boolean(required=True, allow_none=False, error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    is_all_day = fields.Boolean(required=True, allow_none=False, error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    time_start = fields.Integer(required=True, allow_none=True, error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    time_finish = fields.Integer(required=True, allow_none=True, error_messages={'required': ValidationErrorEnum.NOT_FIELD})

    @validates_schema
    def validate_week_day(self, data, **kwargs):
        if data['is_holiday']:
            if data.get('time_start') or data.get('time_finish'):
                raise ValidationError([ValidationErrorEnum.WORK_ON_HOLIDAY])
            if data['is_all_day']:
                raise ValidationError([ValidationErrorEnum.WORK_IN_HOLIDAY])
        elif data['is_all_day']:
            if data.get('time_start') or data.get('time_finish'):
                raise ValidationError([ValidationErrorEnum.WORK_IS_ALL_DAY])
        else:
            if not data['time_start']:
                raise ValidationError({'time_start': ValidationErrorEnum.NOT_FIELD})

            if not data['time_finish']:
                raise ValidationError({'time_finish': ValidationErrorEnum.NOT_FIELD})


class WorkHoursSchema(Schema):
    mo = fields.Dict(fields.String, required=True, allow_none=False, validate=lambda value: WeekDaySchema().load(value), error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    tu = fields.Dict(fields.String, required=True, allow_none=False, validate=lambda value: WeekDaySchema().load(value), error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    we = fields.Dict(fields.String, required=True, allow_none=False, validate=lambda value: WeekDaySchema().load(value), error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    th = fields.Dict(fields.String, required=True, allow_none=False, validate=lambda value: WeekDaySchema().load(value), error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    fr = fields.Dict(fields.String, required=True, allow_none=False, validate=lambda value: WeekDaySchema().load(value), error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    sa = fields.Dict(fields.String, required=True, allow_none=False, validate=lambda value: WeekDaySchema().load(value), error_messages={'required': ValidationErrorEnum.NOT_FIELD})
    su = fields.Dict(fields.String, required=True, allow_none=False, validate=lambda value: WeekDaySchema().load(value), error_messages={'required': ValidationErrorEnum.NOT_FIELD})


class Extra(Schema):
    is_draft = fields.Boolean(required=True, allow_none=False)


class PlacePatchSchema(Schema):
    main_lang_id = fields.Integer(required=False, allow_none=True)
    name = fields.String(required=False, allow_none=True, validate=Length(max=50))
    description = fields.String(required=False, allow_none=True, validate=Length(max=2000))
    login = fields.String(required=False, allow_none=True, validate=Length(max=50))
    photo_link = fields.String(required=False, allow_none=True, validate=Length(max=500))
    place_types_ids = fields.List(fields.Integer, required=False, allow_none=True)
    cuisine_types_ids = fields.List(fields.Integer, required=False, allow_none=True)
    services_ids = fields.List(fields.Integer, required=False, allow_none=True)
    work_hours = fields.Nested(WorkHoursSchema, required=False, allow_none=True)
    main_currency_id = fields.Integer(required=False, allow_none=True)
    location = fields.Nested(LocationSchema, required=False, allow_none=True)
    contacts = fields.Nested(ContactsSchema, required=False, allow_none=True)
    # extra = fields.Nested(Extra, required=True, allow_none=False)

    # @validates_schema
    # def validate_required_params(self, data, **kwargs):
    #     if not data['extra']['is_draft']:
    #         if not data.get('main_lang_id'):
    #             raise ValidationError({'main_lang_id': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('name'):
    #             raise ValidationError({'name': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('description'):
    #             raise ValidationError({'description': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('photo_link'):
    #             raise ValidationError({'photo_link': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('login'):
    #             raise ValidationError({'login': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('place_types_ids'):
    #             raise ValidationError({'place_types_ids': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('cuisine_types_ids'):
    #             raise ValidationError({'cuisine_types_ids': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('services_ids'):
    #             raise ValidationError({'services_ids': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('work_hours'):
    #             raise ValidationError({'work_hours': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('main_currency_id'):
    #             raise ValidationError({'main_currency_id': ValidationErrorEnum.NOT_FIELD})
    #
    #         if not data.get('locations'):
    #             raise ValidationError({'locations': ValidationErrorEnum.NOT_FIELD})
