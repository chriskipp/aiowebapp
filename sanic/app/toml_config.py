#!/usr/bin/env python3

"""This module contains a toml configuration class for sanic."""

from typing import Any, Dict

import toml

from sanic.config import Config


class TomlConfig(Config):  # pylint: disable=W0612
    """TOML configuration class for sanic."""

    def __init__(self, *args, path: str, encoding: str = "UTF-8", **kwargs):
        """
        Initializes a TomlConfig object.

        Attributes:
          path (str): Path to read the configuration from.
          encoding (str): Encoding to use to read configuration file.
        """
        super().__init__(*args, **kwargs)

        with open(path, "r", encoding=encoding) as f:
            self.apply(toml.load(f))

    def apply(self, config):
        """
        Applies the given config object to the configuration.

        Attributes:
          config: Configuration to applie.
        """
        self.update(self._to_uppercase(config))

    def _to_uppercase(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts all keys in the given dictionary to uppercase.

        Attributes:
          obj (dict): Dictionary to read the keys from.
        """
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
