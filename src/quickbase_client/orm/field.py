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
    USER = 600
    OTHER = 900


QB_TEXT = QuickBaseFieldType.TEXT
QB_TEXT_MULTILINE = QuickBaseFieldType.TEXT_MULTILINE
QB_TEXT_MULTIPLE_CHOICE = QuickBaseFieldType.TEXT_MULTIPLE_CHOICE
QB_TEXT_MULTI_SELECT = QuickBaseFieldType.TEXT_MULTI_SELECT
QB_RICH_TEXT = QuickBaseFieldType.RICH_TEXT
QB_NUMERIC = QuickBaseFieldType.NUMERIC
QB_NUMERIC_CURRENCY = QuickBaseFieldType.NUMERIC_CURRENCY
QB_NUMERIC_PERCENT = QuickBaseFieldType.NUMERIC_PERCENT
QB_NUMERIC_RATING = QuickBaseFieldType.NUMERIC_RATING
QB_DATE = QuickBaseFieldType.DATE
QB_DATETIME = QuickBaseFieldType.DATETIME
QB_TIME_OF_DAY = QuickBaseFieldType.TIME_OF_DAY
QB_DURATION = QuickBaseFieldType.DURATION
QB_CHECKBOX = QuickBaseFieldType.CHECKBOX
QB_ADDRESS = QuickBaseFieldType.ADDRESS
QB_EMAIL_ADDRESS = QuickBaseFieldType.EMAIL_ADDRESS
QB_USER = QuickBaseFieldType.USER
QB_OTHER = QuickBaseFieldType.OTHER


_qb_api_type_lookup = {
    'text': QuickBaseFieldType.TEXT,
    'text-multi-line': QuickBaseFieldType.TEXT_MULTILINE,
    'checkbox': QuickBaseFieldType.CHECKBOX,
    'timestamp': QuickBaseFieldType.DATETIME,
    'numeric': QuickBaseFieldType.NUMERIC,
    'date': QuickBaseFieldType.DATE,
    'rich-text': QuickBaseFieldType.RICH_TEXT,
    'text-multiple-choice': QuickBaseFieldType.TEXT_MULTIPLE_CHOICE,
}


def get_field_type_by_string(s):
    return _qb_api_type_lookup.get(s, QuickBaseFieldType.OTHER)


@attr.s(auto_attribs=True)
class QuickBaseField(object):
    fid: int
    field_type: QuickBaseFieldType
    label: str = ''


# FUTURE - could actually store more type-specific field metadata
