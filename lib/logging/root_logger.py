# Copyright (C) 2020 Andy Koch - All Rights Reserved

import logging

_root_logger = logging.getLogger()
_handler = logging.StreamHandler()
_formatter = logging.Formatter(
    "%(asctime)s   "
    "%(levelname)s   "
    "%(name)s   "
    "%(funcName)s()@%(lineno)d   "
    "%(message)s"
)
_handler.setFormatter(_formatter)
_root_logger.addHandler(_handler)
_root_logger.setLevel(logging.INFO)


def get_root_logger() -> logging.Logger:
    return _root_logger
