# -*- coding: utf-8 -*-

from flask import request
from typing import List


class RequestData:
    """ A class that reads the request data, and returns the values in a
    static method-
    """

    @staticmethod
    def get_data() -> str:
        if 'json_data' in request.form and request.form['json_data']:
            return request.form['json_data']
        else:
            return ''

    @staticmethod
    def output_format_in_json() -> bool:
        accept_header = request.headers.get('Accept')
        format_of_output = request.form.get('format_of_output')
        if format_of_output:
            if 'json' in format_of_output:
                return True
        elif accept_header and 'application/json' in accept_header:
            return True
        return False

    @staticmethod
    def client_is_browser(rendering_engines: List[str]) -> bool:
        user_agent_header = request.headers.get('User-Agent')
        if user_agent_header and any(
            rendering_engine in user_agent_header
            for rendering_engine in rendering_engines
        ):
            return True
        return False
