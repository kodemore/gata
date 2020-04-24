import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from inspect import cleandoc
from typing import Any, List, Match, Type, TypeVar, Union

from typing_extensions import Protocol, runtime

T = TypeVar("T")


ISO_8601_DATETIME_REGEX = re.compile(
    r"^(\d{4})-?([0-1]\d)-?([0-3]\d)[t\s]?([0-2]\d:?[0-5]\d:?[0-5]\d|23:59:60|235960)(\.\d+)?(z|[+-]\d{2}:\d{2})?$",
    re.I,
)
ISO_8601_DATE_REGEX = re.compile(r"^(\d{4})-?([0-1]\d)-?([0-3]\d)$", re.I)
ISO_8601_TIME_REGEX = re.compile(
    r"^(?P<time>[0-2]\d:?[0-5]\d:?[0-5]\d|23:59:60|235960)(?P<microseconds>\.\d+)?(?P<tzpart>z|[+-]\d{2}:\d{2})?$", re.I
)

ISO_8601_TIME_DURATION_REGEX = re.compile(
    r"^(?P<sign>-?)P(?=\d|T\d)(?:(?P<weeks>\d+)W)?(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+(?:\.\d+)?)S)?)?$",
    re.I,
)


@runtime
class Comparable(Protocol):  # pragma: no cover
    def __lt__(self, other: Any) -> bool:
        ...

    def __gt__(self, other: Any) -> bool:
        ...

    def __le__(self, other: Any) -> bool:
        return not self > other

    def __ge__(self, other: Any) -> bool:
        return not self < other


def is_typed_dict(value: Any) -> bool:
    if issubclass(value, dict) and hasattr(value, "__annotations__"):
        return True

    return False


def parse_iso_datetime_string(value: str) -> datetime:

    if not ISO_8601_DATETIME_REGEX.match(value):
        raise ValueError(f"passed value {value!r} is not valid ISO-8601 datetime.")

    date_parts = ISO_8601_DATETIME_REGEX.findall(value)[0]
    time_part = date_parts[3]
    if ":" in time_part:
        time_part = time_part.split(":")
    else:
        time_part = list(map("".join, zip(*[iter(time_part)] * 2)))

    if date_parts[5] and date_parts[5].lower() != "z":
        sign = 1 if date_parts[5][0] == "+" else -1
        hours, minutes = date_parts[5][1:].split(":")
        offset = timezone(timedelta(hours=int(hours) * sign, minutes=int(minutes) * sign))
    elif date_parts[5] and date_parts[5].lower() == "z":
        offset = timezone.utc
    else:
        offset = None  # type: ignore

    return datetime(
        year=int(date_parts[0]),
        month=int(date_parts[1]),
        day=int(date_parts[2]),
        hour=int(time_part[0]),
        minute=int(time_part[1]),
        second=int(time_part[2]),
        tzinfo=offset,
    )


def parse_iso_date_string(value: str) -> date:
    if not ISO_8601_DATE_REGEX.match(value):
        raise ValueError("Passed value is not valid ISO-8601 date.")

    date_parts = ISO_8601_DATE_REGEX.findall(value)[0]
    return date(year=int(date_parts[0]), month=int(date_parts[1]), day=int(date_parts[2]))


def parse_iso_duration_string(value: str) -> timedelta:
    """
    Parses duration string according to ISO 8601 and returns timedelta representation (it excludes year and month)
    http://www.datypic.com/sc/xsd/t-xsd_dayTimeDuration.html
    :param str value:
    :return dict:
    """
    if not ISO_8601_TIME_DURATION_REGEX.match(value):
        raise ValueError(f"Passed value {value} is not valid ISO-8601 duration.")

    duration = ISO_8601_TIME_DURATION_REGEX.fullmatch(value)
    sign = -1 if duration.group("sign") else 1  # type: ignore

    kwargs = {
        "weeks": int(duration.group("weeks")) * sign if duration.group("weeks") else 0,  # type: ignore
        "days": int(duration.group("days")) * sign if duration.group("days") else 0,  # type: ignore
        "hours": int(duration.group("hours")) * sign if duration.group("hours") else 0,  # type: ignore
        "minutes": int(duration.group("minutes")) * sign  # type: ignore
        if duration.group("minutes")  # type: ignore
        else 0,
        "seconds": float(duration.group("seconds")) * sign  # type: ignore
        if duration.group("seconds")  # type: ignore
        else 0,
    }

    return timedelta(**kwargs)  # type: ignore


def parse_iso_time_string(value: str) -> time:
    if not ISO_8601_TIME_REGEX.match(value):
        raise ValueError(f"Passed value {value} is not valid ISO-8601 time.")

    time_parts = ISO_8601_TIME_REGEX.fullmatch(value)
    hour_parts = time_parts.group("time")  # type: ignore
    if ":" in hour_parts:
        hour_parts = hour_parts.split(":")
    else:
        hour_parts = list(map("".join, zip(*[iter(hour_parts)] * 2)))

    microseconds = time_parts.group("microseconds")  # type: ignore
    if microseconds is not None:
        microseconds = int(microseconds[1:])
    else:
        microseconds = 0

    tz_part = time_parts.group("tzpart")  # type: ignore
    if tz_part and tz_part.lower() != "z":
        sign = 1 if tz_part[0] == "+" else -1
        hours, minutes = tz_part[1:].split(":")
        offset = timezone(timedelta(hours=int(hours) * sign, minutes=int(minutes) * sign))
    elif tz_part and tz_part.lower() == "z":
        offset = timezone.utc
    else:
        offset = None  # type: ignore

    return time(
        hour=int(hour_parts[0]),
        minute=int(hour_parts[1]),
        second=int(hour_parts[2]),
        microsecond=microseconds,
        tzinfo=offset,
    )


def timedelta_to_iso_string(value: timedelta) -> str:
    seconds = value.total_seconds()
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    weeks, days, hours, minutes = map(int, (weeks, days, hours, minutes))
    seconds = round(seconds, 6)

    iso_8601 = sign + "P"
    iso_8601_date = ""
    iso_8601_time = ""
    if weeks:
        iso_8601_date += f"{weeks}W"

    if days:
        iso_8601_date += f"{days}D"

    if hours:
        iso_8601_time += f"{hours}H"

    if minutes:
        iso_8601_time += f"{minutes}M"

    if seconds:
        if seconds.is_integer():
            iso_8601_time += f"{int(seconds)}S"
        else:
            iso_8601_time += f"{seconds}S"

    return f"{iso_8601}{iso_8601_date}" + (f"T{iso_8601_time}" if iso_8601_time else "")


class DocComponent:
    def __init__(self, component_type: str, attributes: List[str], description: str = ""):
        self.type = component_type
        self.attributes = attributes
        self.description = description


DOC_COMPONENT_REGEX = re.compile(r"^:([^:]+):(.*?)$", re.I | re.M)


class DocString:
    """
    Simple ReST doc string parser.
    """

    def __init__(self, target: Any):
        """
        Reads doc string of classes and functions and parses it into components.
        """
        self.raw_doc = cleandoc(target.__doc__ or "")
        self._components: List[DocComponent] = []
        self._short_description = ""
        self._long_description = ""
        self._parse()

    @property
    def components(self) -> List[DocComponent]:
        return self._components

    def find_component_by_type(self, *component_type: str) -> List[DocComponent]:
        result = []
        for component in self._components:
            if component.type in component_type:
                result.append(component)
                continue

        return result

    @property
    def short_description(self) -> str:
        return self._short_description

    @property
    def long_description(self) -> str:
        return self._long_description

    def _parse(self) -> None:
        parts = self.raw_doc.split("\n")
        description: List[str] = []
        components: List[DocComponent] = []

        for part in parts:  # type: str
            clean_part: str = part.strip()

            matches = DOC_COMPONENT_REGEX.match(clean_part)
            if matches:
                component = self._parse_component(matches)
                components.append(component)
                continue

            description.append(part)

        if description:
            self._long_description = "\n".join(description[1:]).strip("\n")
            self._short_description = description[0]
        self._components = components

    def _parse_component(self, matches: Match[str]) -> DocComponent:
        component_parts = matches[1].split(" ")
        if len(component_parts) > 1:
            return DocComponent(component_parts[0], component_parts[1:], matches[2].strip())
        else:
            return DocComponent(component_parts[0], [], matches[2].strip())


def noop(value: Any) -> Any:
    return value


NoneType = type(None)


def is_optional_type(type_: Any) -> bool:
    origin_type = getattr(type_, "__origin__", None)

    if not origin_type:
        return False
    if origin_type != Union:
        return False

    return NoneType in type_.__args__  # type: ignore


def convert_to_dataclass(cls: Type[T]) -> Type[T]:
    return dataclass(cls, init=False, repr=False, eq=False)  # type: ignore


__all__ = [
    "convert_to_dataclass",
    "Comparable",
    "is_typed_dict",
    "parse_iso_datetime_string",
    "parse_iso_date_string",
    "parse_iso_duration_string",
    "parse_iso_time_string",
    "DocString",
    "timedelta_to_iso_string",
    "noop",
    "NoneType",
    "is_optional_type",
]
