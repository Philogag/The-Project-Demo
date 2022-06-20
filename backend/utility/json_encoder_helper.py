from abc import abstractmethod
from datetime import datetime, date

from flask.json import JSONEncoder


class JsonEncoderPlugin:
    @classmethod
    @abstractmethod
    def encode(cls, obj):
        """:return: `None` if not fit"""
        pass


class DateTimeEncoderPlugin(JsonEncoderPlugin):
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return None


class CustomJsonEncoder(JSONEncoder):

    __plugins__ = [
        DateTimeEncoderPlugin,
    ]

    def default(self, obj):
        for plugin in self.__plugins__:
            result = plugin.encode(obj)
            if result is not None:
                return result
        return JSONEncoder.default(self, obj)
