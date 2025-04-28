from starlette_admin.exceptions import FormValidationError

from .app_time import current_time_with_timezone, make_datetime_timezone_aware


def validate_datetime_field(data: dict, obj) -> None:
    """Валидация полей datetime при создании и редактировании в админке."""
    datetime_data = data.get('datetime')
    if not datetime_data:
        raise FormValidationError(
            errors={
                'datetime': 'Дата не может быть пустой.'})
    datetime_data = make_datetime_timezone_aware(datetime_data)
    datetime_current = current_time_with_timezone()
    if datetime_data <= datetime_current:
        raise FormValidationError(
            errors={
                'datetime': 'Дата должна быть в будущем.'})
