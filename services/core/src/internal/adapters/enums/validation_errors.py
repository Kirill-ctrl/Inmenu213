from src.internal.adapters.entities.validation_error import ValidationError
from src.internal.biz.services.answer_service import AnswerService
from src.service.meta.class_property import classproperty


class ValidationErrorEnum:

    @classproperty
    def EMPTY_BODY(cls) -> ValidationError:
        return AnswerService.get_error_empty_body()

    @classproperty
    def UNKNOWN_FIELD(cls) -> ValidationError:
        return AnswerService.get_error_unknown_field()

    @classproperty
    def NULL_FIELD(cls) -> ValidationError:
        return AnswerService.get_error_null_field()

    @classproperty
    def NOT_FIELD(cls) -> ValidationError:
        return AnswerService.get_error_not_field()

    @classproperty
    def WRONG_TYPE_FIELD(cls) -> ValidationError:
        return AnswerService.get_error_wrong_type_field()

    @classproperty
    def WRONG_CODE_FORMAT(cls) -> ValidationError:
        return AnswerService.get_error_invalid_code_format()

    @classproperty
    def WORK_ON_HOLIDAY(cls) -> ValidationError:
        return AnswerService.get_error_work_on_holiday()

    @classproperty
    def NOT_GMAIL(cls) -> ValidationError:
        return AnswerService.get_error_not_gmail()

    @classproperty
    def WORK_IN_HOLIDAY(cls) -> ValidationError:
        return AnswerService.get_error_work_in_holiday()

    @classproperty
    def WORK_IS_ALL_DAY(cls) -> ValidationError:
        return AnswerService.get_error_work_is_all_day()
