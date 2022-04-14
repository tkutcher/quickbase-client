from enum import Enum

import attr


class QuickbaseFieldType(Enum):
    """An Enumeration of Field Types.

    .. note::
        Formula fields use the underlying type.

    In the generated classes, the import for this class is usually aliased
    as ``Qb`` to make it easier to write like ``Qb.TEXT``.

    These also all have constants in ``quickbase_client.orm.field`` module prefixed with
    ``QB_``.
    """

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


QuickBaseFieldType = QuickbaseFieldType  # alias - TODO - delete in future


QB_TEXT = QuickbaseFieldType.TEXT
QB_TEXT_MULTILINE = QuickbaseFieldType.TEXT_MULTILINE
QB_TEXT_MULTIPLE_CHOICE = QuickbaseFieldType.TEXT_MULTIPLE_CHOICE
QB_TEXT_MULTI_SELECT = QuickbaseFieldType.TEXT_MULTI_SELECT
QB_RICH_TEXT = QuickbaseFieldType.RICH_TEXT
QB_NUMERIC = QuickbaseFieldType.NUMERIC
QB_NUMERIC_CURRENCY = QuickbaseFieldType.NUMERIC_CURRENCY
QB_NUMERIC_PERCENT = QuickbaseFieldType.NUMERIC_PERCENT
QB_NUMERIC_RATING = QuickbaseFieldType.NUMERIC_RATING
QB_DATE = QuickbaseFieldType.DATE
QB_DATETIME = QuickbaseFieldType.DATETIME
QB_TIME_OF_DAY = QuickbaseFieldType.TIME_OF_DAY
QB_DURATION = QuickbaseFieldType.DURATION
QB_CHECKBOX = QuickbaseFieldType.CHECKBOX
QB_ADDRESS = QuickbaseFieldType.ADDRESS
QB_EMAIL_ADDRESS = QuickbaseFieldType.EMAIL_ADDRESS
QB_USER = QuickbaseFieldType.USER
QB_OTHER = QuickbaseFieldType.OTHER


_qb_api_type_lookup = {
    "text": QuickbaseFieldType.TEXT,
    "text-multi-line": QuickbaseFieldType.TEXT_MULTILINE,
    "multitext": QuickbaseFieldType.TEXT_MULTI_SELECT,
    "checkbox": QuickbaseFieldType.CHECKBOX,
    "timestamp": QuickbaseFieldType.DATETIME,
    "numeric": QuickbaseFieldType.NUMERIC,
    "currency": QuickbaseFieldType.NUMERIC_CURRENCY,
    "percent": QuickbaseFieldType.NUMERIC_PERCENT,
    "rating": QuickbaseFieldType.NUMERIC_RATING,
    "duration": QuickbaseFieldType.DURATION,
    "date": QuickbaseFieldType.DATE,
    "timeofday": QuickbaseFieldType.TIME_OF_DAY,
    "rich-text": QuickbaseFieldType.RICH_TEXT,
    "text-multiple-choice": QuickbaseFieldType.TEXT_MULTIPLE_CHOICE,
}


def get_field_type_by_string(s):
    return _qb_api_type_lookup.get(s, QuickbaseFieldType.OTHER)


@attr.s(auto_attribs=True)
class QuickbaseField(object):
    """The metadata for a specific field.

    :var int fid: The field id.
    :ivar QuickbaseFieldType field_type: The :class:`~QuickbaseFieldType` of the field.
    :ivar str label: The label for the field.
    :ivar Optional[str] formula: The Quickbase string formula.
    """

    fid: int
    field_type: QuickbaseFieldType
    label: str = ""
    formula: str = None

    @property
    def is_formula(self):
        return self.formula is not None and self.formula != ""


# FUTURE - could actually store more type-specific field metadata

QuickBaseField = QuickbaseField  # alias - TODO - delete in future
