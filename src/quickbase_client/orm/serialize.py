import abc
import json
from datetime import date
from datetime import datetime
from typing import Dict
from typing import Type

from quickbase_client.orm.field import QuickbaseFieldType
from quickbase_client.orm.table import QuickbaseTable
from quickbase_client.utils.string_utils import normalize_unicode


# TODO - encoder should be build dynamically from app date props.


class QuickbaseJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat().split(".")[0]
        elif isinstance(o, date):
            return o.isoformat()
        return super().default(o)  # pragma: no cover


class RecordSerializer(abc.ABC):
    @abc.abstractmethod
    def serialize(self, record: "QuickbaseTable"):
        pass  # pragma: no cover

    @abc.abstractmethod
    def deserialize(self, data):
        pass  # pragma: no cover


class RecordJsonSerializer(RecordSerializer):
    def __init__(self, table_cls: Type[QuickbaseTable], normalize_unicode: bool = True):
        self.table_cls = table_cls
        self.normalize_unicode = normalize_unicode

    def serialize(self, record: "QuickbaseTable") -> Dict:
        o = {}
        for attr, v in record.__dict__.items():
            if attr[0] == "_" or v is None:
                continue
            field_info = record.get_field_info(attr)
            if field_info.field_type == QuickbaseFieldType.DATE and isinstance(
                v, datetime
            ):
                v = v.date()
            if (
                self.normalize_unicode
                and field_info.field_type
                in [
                    QuickbaseFieldType.TEXT,
                    QuickbaseFieldType.TEXT_MULTILINE,
                    QuickbaseFieldType.TEXT_MULTI_SELECT,
                    QuickbaseFieldType.TEXT_MULTIPLE_CHOICE,
                ]
                and isinstance(v, str)
            ):
                v = normalize_unicode(v)
            o[field_info.fid] = {"value": v}
        return o

    def deserialize(self, data):
        c = self.table_cls()
        for fid, v in data.items():
            a = c.get_attr_from_fid(int(fid))
            field_info = c.get_field_info(a)

            # could be cleaner elsewhere
            try:
                if field_info.field_type == QuickbaseFieldType.DATE:
                    val = datetime.strptime(v["value"], "%Y-%m-%d").date()
                elif field_info.field_type == QuickbaseFieldType.DATETIME:
                    val = datetime.fromisoformat(v["value"].rstrip("Z"))
                else:
                    val = v["value"]
            except (ValueError, KeyError):
                val = None
            setattr(c, a, val)

        return c
