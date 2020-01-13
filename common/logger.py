# -*- coding: utf-8 -*-

import datetime
import logging


class Logger:
    """A basic class that logs a message (via a static method) with the
    logging module.
    """

    @staticmethod
    def log_error(msg: str) -> None:
        logging.error(f'{datetime.datetime.now()} => {msg}')

    @staticmethod
    def log_warning(msg: str) -> None:
        logging.warning(f'{datetime.datetime.now()} => {msg}')
