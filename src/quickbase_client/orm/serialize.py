import abc
from datetime import datetime
from datetime import date
import json
from typing import Dict
from typing import Type

from quickbase_client.orm.field import QuickBaseFieldType
from quickbase_client.orm.table import QuickBaseTable


class QuickBaseJsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()
        return super().default(o)  # pragma: no cover


class RecordSerializer(abc.ABC):

    @abc.abstractmethod
    def serialize(self, record: 'QuickBaseTable'):
        pass  # pragma: no cover

    @abc.abstractmethod
    def deserialize(self, data):
        pass  # pragma: no cover


class RecordJsonSerializer(RecordSerializer):

    def __init__(self, table_cls: Type[QuickBaseTable]):
        self.table_cls = table_cls

    def serialize(self, record: 'QuickBaseTable') -> Dict:
        o = {}
        for attr, v in record.__dict__.items():
            if attr[0] == '_' or v is None:
                continue
            field_info = record.get_field_info(attr)
            o[field_info.fid] = {'value': v}
        return o

    def deserialize(self, data):
        c = self.table_cls()
        for fid, v in data.items():
            a = c.get_attr_from_fid(int(fid))
            field_info = c.get_field_info(a)

            # could be cleaner elsewhere
            if field_info.field_type == QuickBaseFieldType.DATE:
                val = datetime.strptime(v['value'], '%Y-%m-%d').date()
            elif field_info.field_type == QuickBaseFieldType.DATETIME:
                val = datetime.fromisoformat(v['value'].rstrip('Z'))
            else:
                val = v['value']
            setattr(c, a, val)

        return c
