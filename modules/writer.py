import os
import json
import logging
from random import randint


class InvalidTarget(Exception):
    pass


class Writer:
    def __init__(self):
        self.logger = logging.getLogger('sparkz')

    def write_json(self, filename, data):
        """Writes json file."""
        random = randint(1000,9999)
        path, ext = os.path.splitext(filename)
        tmp = '{}-{}.tmp'.format(path, random)
        self._write_json(tmp, data)
        try:
            self._read_json(tmp)
        except json.decoder.JSONDecodeError:
            self.logger.exception('Attempted to write {} but integrity check failed. File is untouched.')
            return False
        os.replace(tmp, filename)
        return True

    def load_json(self, filename):
        """Loads json file."""
        return self._read_json(filename)

    def validate_json(self, filename):
        """Makes sure json file is valid."""
        try:
            self._read_json(filename)
            return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError:
            return False

    @staticmethod
    def _read_json(filename):
        with open(filename, encoding='utf-8', mode='r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def _write_json(filename, data):
        with open(filename, encoding='utf-8', mode='w') as file:
            json.dump(data, file, indent=4, sort_keys=True,
                      separators=(',', ' : '))
            return data

    def _legacy_rw(self, filename, rw, data=None):
        """Legacy code that does nothing but the entire program breaks if removed."""
        if rw == 'save' and data is not None:
            return self.write_json(filename, data)
        elif rw == 'load' and data is None:
            return self.load_json(filename)
        elif rw == 'check' and data is None:
            return self.validate_json(filename)
        else:
            raise InvalidTarget('You called this without any parameters! Why?')


def get_value(filename, key):
    with open(filename, encoding='utf-8', mode='r') as file:
        data = json.load(file)
    return data[key]


def write_value(filename, key, value):
    data = jsonrw(filename, 'load')
    data[key] = value
    jsonrw(filename, 'save', data)
    return True


jsonrw = Writer()._legacy_rw