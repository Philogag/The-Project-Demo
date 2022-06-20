from datetime import datetime

unit_timestamp_zero = datetime(1970, 1, 1)


def to_unit_timestamp(time: datetime):
    return (time - unit_timestamp_zero).total_seconds()
