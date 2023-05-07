import abc
import os.path
from typing import TypeVar
import warnings

import json

from dataclass_factory import Factory


class JsonSerializableProtocol:
    pass


_T = TypeVar("_T")


class StateError(Exception):
    pass


class StateNotLoaded(StateError):
    pass


class StatePlaceholder:
    def __init__(self, name: str):
        self.name = name


def get_state_object_name(obj) -> str:
    return getattr(obj, '__state_name__')


class StateStorage:
    @abc.abstractmethod
    def load(self) -> dict:
        pass

    @abc.abstractmethod
    def save(self, data: dict) -> None:
        pass


class JsonStateStorage(StateStorage):
    def __init__(self, filename: str):
        self._filename = filename

    def load(self):
        if not os.path.exists(self._filename):
            return dict()

        with open(self._filename, 'r') as fs:
            data = json.load(fs)

        return data

    def save(self, data: dict) -> None:
        with open(self._filename, 'w') as fs:
            json.dump(data, fs)

        return None


class LongStateObjectMixin:
    __type_registry: dict

    def __init__(self, storage: StateStorage):
        self._storage = storage
        self._is_open = False
        self.__obj_registry = dict()

    def __init_subclass__(cls, **kwargs):
        cls.__type_registry = dict()

        for name, obj in vars(cls).items():
            if isinstance(obj, StatePlaceholder):
                cls.__type_registry.update({name: cls.__annotations__[name]})

    def open(self):
        data = self._storage.load()

        for name, tp in self.__type_registry.items():
            if data.get(name) is None:
                try:
                    obj = tp()
                except Exception as e:
                    raise ValueError(f"Can't detect initial state of state object `{name}` (type: `{tp}`)") from e
            else:
                factory = Factory()
                obj = factory.load(data[name], tp)

            setattr(self, name, obj)
            self.__obj_registry.update({name: obj})

        self._is_open = True

    def close(self):
        data = dict()

        for name, obj in self.__obj_registry.items():
            factory = Factory()
            data.update({name: factory.dump(obj)})
            setattr(self, name, StatePlaceholder(name=name))

        self._storage.save(data)

        self._is_open = False

    def __del__(self):
        if self._is_open:
            self.close()
            warnings.warn(
                Warning(f"Executor `{self}` was not explicitly closed")
            )

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
