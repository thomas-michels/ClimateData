from datetime import datetime

from backend.app.exceptions import UnprocessableEntityException


def check_is_future_date(date_check: datetime):

    if date_check > datetime.today():
        raise UnprocessableEntityException('A data é futura')
