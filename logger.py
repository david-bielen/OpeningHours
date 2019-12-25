# -*- coding: utf-8 -*-

import logging


class Logger:
    """A class that logs a message (via a static method) with the logging
    module.
    """

    @staticmethod
    def log_error(msg: str) -> None:
        logging.basicConfig(format='ERROR: %(asctime)s => %(msg)s')
        logging.error(msg)

    @staticmethod
    def log_warning(msg: str) -> None:
        logging.basicConfig(format='WARNING: %(asctime)s => %(msg)s')
        logging.error(msg)
