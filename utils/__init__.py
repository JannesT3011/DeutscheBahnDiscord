from .get_route_data import get_station_info, get_journey_info
from .get_trips_data import get_trip_id, get_trip_info
from .get_stops_data import get_departure_data

from datetime import datetime
from dateutil import parser

def format_dt(time) -> str:
    """
    FORMAT API TIME (e.g: 2023-02-25T16:48:00+01:00)
    TO: "%d.%m.%y %H:%M" format (str)
    """
    dt_parser = parser.isoparse(time)

    return datetime.strftime(dt_parser, "%d.%m.%y %H:%M")


def calc_delay(planned: str, actual: str) -> int:
    """
    CALC THE DELAY (DELTA) BETWEEN TO GIVEN TIMES
    """
    planned_dt = datetime.strptime(planned, "%d.%m.%y %H:%M")
    actual_dt = datetime.strptime(actual, "%d.%m.%y %H:%M")

    return int((actual_dt - planned_dt).seconds / 60)

def str_to_time(str_time) -> datetime: # Input: DD.MM.YY hh:mm
    """
    FORMAT API TIME TO DATETIME
    TO: "%d.%m.%y %H:%M" format
    """
    return datetime.strptime(str_time, "%d.%m.%y %H:%M")