import abc
import datetime
import json
from datetime import date
from typing import Dict

from quickbase_client.orm.table import QuickBaseTable


class QuickBaseJsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, date):
            return o.isoformat()
        if isinstance(o, bool):
            return o
        return super().default(o)


class RecordSerializer(abc.ABC):

    @abc.abstractmethod
    def serialize(self, record: 'QuickBaseTable'):
        pass

    @abc.abstractmethod
    def deserialize(self, data):
        pass


class RecordJsonSerializer(RecordSerializer):

    def serialize(self, record: 'QuickBaseTable') -> Dict:
        o = {}
        for attr, v in record.__dict__.items():
            field_info = record.get_field_info(attr)
            o[field_info.fid] = {'value': v}
        return o

    def deserialize(self, data):
        pass
