from src.internal.adapters.entities.error import Error
from src.internal.biz.services.answer_service import AnswerService
from src.service.meta.class_property import classproperty


class ErrorEnum:

    @classproperty
    def NOT_UNIQUE_EMAIL(cls) -> Error:
        return AnswerService.get_error_not_unique_email()

    @classproperty
    def WRONG_EMAIL_PASSWORD(cls) -> Error:
        return AnswerService.get_error_wrong_email_password()

    @classproperty
    def FORBIDDEN(cls) -> Error:
        return AnswerService.get_error_forbidden()

    @classproperty
    def INVALID_OR_OUTDATED_TOKEN(cls) -> Error:
        return AnswerService.get_error_invalid_or_outdated_token()

    @classproperty
    def UNKNOWN_CODE(cls) -> Error:
        return AnswerService.get_error_unknown_code()

    @classproperty
    def LIFETIME_CODE_OUT(cls) -> Error:
        return AnswerService.get_error_lifetime_code_out()

    @classproperty
    def SEND_CODE_TOO_OFTEN(cls) -> Error:
        return AnswerService.get_error_send_code_too_often()

    @classproperty
    def WRONG_LANGUAGE(cls) -> Error:
        return AnswerService.get_error_wrong_language()

    @classproperty
    def NOT_UNIQUE_PLACE_LOGIN(cls) -> Error:
        return AnswerService.get_not_unique_place_login()

    @classproperty
    def WRONG_CUISINE_TYPE(cls) -> Error:
        return AnswerService.get_wrong_cuisine_type()

    @classproperty
    def WRONG_PLACE_TYPE(cls) -> Error:
        return AnswerService.get_wrong_place_type()

    @classproperty
    def WRONG_SERVICE(cls) -> Error:
        return AnswerService.get_wrong_service()

    @classproperty
    def WRONG_PHONE_NUMBER_FORMAT(cls) -> Error:
        return AnswerService.get_wrong_phone_number_format()

    @classproperty
    def WRONG_CURRENCY(cls) -> Error:
        return AnswerService.get_wrong_currency()

    @classproperty
    def EMAIL_IS_NOT_CONFIRMED(cls) -> Error:
        return AnswerService.get_error_email_is_not_confirmed()

    @classproperty
    def EMAIL_IS_ALREADY_CONFIRMED(cls) -> Error:
        return AnswerService.get_error_email_is_already_confirmed()

    @classproperty
    def PLACE_DOESNT_EXISTS(cls) -> Error:
        return AnswerService.get_error_place_doesnt_exists()

    @classproperty
    def PLACE_FORBIDDEN(cls) -> Error:
        return AnswerService.get_error_place_forbidden()

    @classproperty
    def MEASURE_UNIT_DOESNT_EXISTS(cls) -> Error:
        return AnswerService.get_error_measure_doesnt_exists()

    @classproperty
    def MENU_CATEGORY_DOESNT_EXISTS(cls) -> Error:
        return AnswerService.get_error_menu_category_exists()

    @classproperty
    def MENU_MAIN_DOESNT_EXISTS(cls) -> Error:
        return AnswerService.get_error_menu_main_doesnt_exists()

    @classproperty
    def UNKNOWN_ERROR(cls) -> Error:
        return AnswerService.get_unkmown_error()

    @classproperty
    def NOT_FOUND(cls) -> Error:
        return AnswerService.get_error_not_found()

    @classproperty
    def DISHES_DOESNT_EXISTS(cls) -> Error:
        return AnswerService.get_error_dishes_doesnt_exists()

    @classproperty
    def DISH_MEASURE_VALUE_AND_PRICE_DOESNT_EXISTS(cls) -> Error:
        return AnswerService.get_error_dish_measure_value_and_price_doesnt_exists()

    @classproperty
    def LANGUAGE_DOESNT_EXISTS(cls) -> Error:
        return AnswerService.get_error_language_doesnt_exists()

    @classproperty
    def CURRENCY_DOESNT_EXISTS(cls) -> Error:
        return AnswerService.get_error_currency_doesnt_exists()

    @classproperty
    def STATUS_DOESNT_MATCH(cls) -> Error:
        return AnswerService.get_error_place_forbidden()

    @classproperty
    def STATUS_IS_UNDEFINED(cls) -> Error:
        return AnswerService.get_error_status_is_undefined()

    @classproperty
    def UNIQUE_PLACE_TYPE(cls) -> Error:
        return AnswerService.get_error_unique_place_type()

    @classproperty
    def UNIQUE_PLACE_SERVICE(cls) -> Error:
        return AnswerService.get_error_unique_place_service()