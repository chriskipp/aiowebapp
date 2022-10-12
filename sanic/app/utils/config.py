#!/usr/bin/env python3

import toml
import yaml

from sanic.config import Config


class XxmlConfig(Config):
    def apply(self, config):
        self.update(self._to_uppercase(config))

    def _to_uppercase(self, obj):
        retval: Dict[str, Any] = {}
        for key, value in obj.items():
            upper_key = key.upper()
            if isinstance(value, list):
                retval[upper_key] = [
                    self._to_uppercase(item) for item in value
                ]
            elif isinstance(value, dict):
                retval[upper_key] = self._to_uppercase(value)
            else:
                retval[upper_key] = value
        return retval


class YamlConfig(XxmlConfig):
    def __init__(self, *args, path: str, **kwargs):
        super().__init__(*args, **kwargs)

        with open(path, "r") as f:
            self.apply(yaml.load(f, Loader=yaml.SafeLoader))


class TomlConfig(XxmlConfig):
    def __init__(self, *args, path: str, **kwargs):
        super().__init__(*args, **kwargs)

        with open(path, "r") as f:
            self.apply(toml.load(f))
