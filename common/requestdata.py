# -*- coding: utf-8 -*-

from flask import request


class RequestData:
    """ A class that reads the request data, and returns the values in a
    static method.
    """

    @staticmethod
    def get_post_value(param: str) -> str:
        if param in request.form and request.form[param]:
            return request.form[param]
        else:
            return ''

    @staticmethod
    def get_header_value(header: str) -> str:
        if header in request.headers and request.headers[header]:
            return request.headers[header]
        else:
            return ''
