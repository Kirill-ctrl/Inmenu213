from src.internal.adapters.entities.error import Error
from src.internal.adapters.entities.validation_error import ValidationError
from src.internal.biz.services.base_service import BaseService


class AnswerService(BaseService):
    # Validation errors

    @staticmethod
    def get_error_empty_body():
        return ValidationError(-101, 'Отправлено пустое тело запроса', 400)

    @staticmethod
    def get_error_unknown_field():
        return ValidationError(-102, 'Введено неизвестное поле: ', 400)

    @staticmethod
    def get_error_not_field():
        return ValidationError(-103, 'Отсутствует поле: ', 400)

    @staticmethod
    def get_error_wrong_type_field():
        return ValidationError(-104, 'Некорректный тип поля: ', 400)

    @staticmethod
    def get_error_null_field():
        return ValidationError(-105, 'Поле не может принимать значение null: ', 400)

    @staticmethod
    def get_error_invalid_code_format():
        return ValidationError(-106, 'Формат кода должен иметь вид: XXXXXX', 400)

    @staticmethod
    def get_error_work_on_holiday():
        return ValidationError(-107, 'В выходной день не может быть указано время работы', 400)

    @staticmethod
    def get_wrong_phone_number_format():
        return ValidationError(-108, 'Формат номера телефона должен иметь вид: 7XXXXXXXXXX: ', 400)

#     ==================================================================================
#     Auth errors

    @staticmethod
    def get_error_not_unique_email():
        return Error(-201, 'Данный email уже занят', 400)

    @staticmethod
    def get_error_wrong_email_password():
        return Error(-202, 'Неправильный логин или пароль', 400)

    @staticmethod
    def get_error_forbidden():
        return Error(-203, 'Запрос недоступен неавторизованным пользователям', 401)

    @staticmethod
    def get_error_invalid_or_outdated_token() -> Error:
        return Error(-204, 'Невалидный или устаревший токен', 401)

    @staticmethod
    def get_error_unknown_code() -> Error:
        return Error(-205, 'Указан неизвестный код подтверждения', 400)

    @staticmethod
    def get_error_lifetime_code_out() -> Error:
        return Error(-206, 'Время действия кода истекло', 400)

    @staticmethod
    def get_error_send_code_too_often() -> Error:
        return Error(-207, f'Сообщения можно отправлять не чаще, чем раз в 60 секунд', 400)

    @staticmethod
    def get_error_email_is_not_confirmed() -> Error:
        return Error(-208, 'Вы не можете выполнить данное действие, пока не подтвердите почту', 400)

#     ==================================================================================
#     Places errors

    @staticmethod
    def get_error_wrong_language() -> Error:
        return Error(-301, 'Указан неверный язык', 400)

    @staticmethod
    def get_not_unique_place_login() -> Error:
        return Error(-302, 'Данный логин уже занят', 400)

    @staticmethod
    def get_wrong_cuisine_type() -> Error:
        return Error(-302, 'Указан неверный id типа кухни', 400)

    @staticmethod
    def get_wrong_place_type() -> Error:
        return Error(-303, 'Указан неизвестный id типа места', 400)

    @staticmethod
    def get_wrong_service() -> Error:
        return Error(-304, 'Указан неизвестный id услуги', 400)

    @staticmethod
    def get_wrong_currency() -> Error:
        return Error(-305, 'Указан неизвестный id валюты', 400)

    @staticmethod
    def get_error_place_doesnt_exists() -> Error:
        return Error(-306, 'Данное заведение не существует', 400)

    @staticmethod
    def get_error_place_forbidden() -> Error:
        return Error(-307, 'Нет доступа к данному заведению', 400)

    @staticmethod
    def get_error_measure_doesnt_exists() -> Error:
        return Error(-308, 'Данная единица измерения объема не существует', 400)

    @staticmethod
    def get_error_menu_category_exists() -> Error:
        return Error(-309, 'Данная категория меню не существует', 400)

    @staticmethod
    def get_error_menu_main_doesnt_exists() -> Error:
        return Error(-310, 'Дааное меню не существует', 400)

    @staticmethod
    def get_error_menu_doesnt_exists() -> Error:
        return Error(-310, 'Данное меню не существует', 400)