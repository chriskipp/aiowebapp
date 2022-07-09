# settings.py
import argparse
import pathlib

import trafaret as t
from trafaret_config import commandline

TRAFARET = t.Dict(
    {
        t.Key("postgres"): t.Dict(
            {
                "database": t.String(),
                "user": t.String(),
                "password": t.String(),
                "host": t.String(),
                "port": t.Int(),
                "minsize": t.Int(),
                "maxsize": t.Int(),
            }
        ),
        t.Key("postgres_sa"): t.Dict(
            {
                "database": t.String(),
                "user": t.String(),
                "password": t.String(),
                "host": t.String(),
                "port": t.Int(),
                "minsize": t.Int(),
                "maxsize": t.Int(),
            }
        ),
        t.Key("redis"): t.Dict(
            {
                "host": t.String(),
                "port": t.Int(),
                "minsize": t.Int(),
                "maxsize": t.Int(),
            }
        ),
        t.Key("host"): t.IP,
        t.Key("port"): t.Int(),
    }
)

BASE_DIR = pathlib.Path(__file__).parent.parent
# BASE_DIR = pathlib.Path(__file__).parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config" / "test.yaml"


def get_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap, default_config=DEFAULT_CONFIG_PATH
    )

    # ignore unknown options
    options, unknown = ap.parse_known_args(argv)

    return commandline.config_from_options(options, TRAFARET)
