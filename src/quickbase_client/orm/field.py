from enum import Enum

import attr


class QuickBaseFieldType(Enum):
    TEXT = 100
    TEXT_MULTILINE = 101
    TEXT_MULTIPLE_CHOICE = 102
    TEXT_MULTI_SELECT = 102
    RICH_TEXT = 103
    NUMERIC = 200
    NUMERIC_CURRENCY = 201
    NUMERIC_PERCENT = 202
    NUMERIC_RATING = 203
    DATE = 300
    DATETIME = 301
    TIME_OF_DAY = 302
    DURATION = 303
    CHECKBOX = 400
    ADDRESS = 500
    EMAIL_ADDRESS = 501
    OTHER = 900


@attr.s(auto_attribs=True)
class QuickBaseField(object):
    fid: int
    field_type: QuickBaseFieldType


# FUTURE - could actually store all of the field metadata here, for now just
#   enumerating the types.
