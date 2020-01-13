# -*- coding: utf-8 -*-

from time import gmtime
import json
import jsonschema  # type: ignore
from typing import Dict, List, Union, Optional, TypeVar
from time import strftime
from common.logger import Logger  # type: ignore


# Type aliases
SI = TypeVar('SI', str, int)
DayElementType = List[Dict[str, SI]]
MainObjectType = Dict[str, DayElementType]


class OpeningHours:
    """A class that validates JSON input representing the opening hours
    of a restaurant, and encodes the input into a human readable format
    of the opening hours, formatted using 12-hour clock.
    """

    def __init__(
        self,
        post_value_json_data: str,
        post_value_format_of_output: str,
        header_value_accept: str,
        header_value_user_agent: str,
        schema: object,
        ordered_days: List[str],
        rendering_engines: List[str]
    ) -> None:
        self.post_value_json_data = post_value_json_data
        self.post_value_format_of_output = post_value_format_of_output
        self.header_value_accept = header_value_accept
        self.header_value_user_agent = header_value_user_agent
        self.schema = schema
        self.ordered_days = ordered_days
        self.ordered_days_last_day_shifted = ordered_days[1:] \
            + ordered_days[:1]
        self.rendering_engines = rendering_engines
        self.error_respons: str
        self.client_is_browser = self.__client_browser()
        self.json_out = self.__output_format_in_json()

    def __validate_input(self) -> bool:
        if not self.__validate_json():
            return False

        if not self.__validate_schema():
            return False

        if not self.__validate_open_close_order():
            return False

        return True

    def __validate_json(self) -> bool:
        """Verify if the input string is valid json."""
        try:
            self.json_object: Dict = json.loads(self.post_value_json_data)
            return True
        except json.decoder.JSONDecodeError as err:
            self.error_respons = \
                f'Input is not valid JSON. {repr(err)}'
            Logger.log_error(self.error_respons)
            return False
        except Exception as err:
            self.error_respons = (
                f'Non-defined exception while validating JSON: '
                f'{repr(err)}'
            )
            Logger.log_error(self.error_respons)
            return False

    def __validate_schema(self) -> bool:
        """Verify if the json object adheres to our schema."""
        try:
            jsonschema.validate(self.json_object, self.schema)
            return True
        except jsonschema.ValidationError as err:
            self.error_respons = (f'Invalid schema: {err.message}')
            Logger.log_error(self.error_respons)
            return False
        except Exception as err:
            self.error_respons = (
                f'Undefined exception while validating schema: '
                f'{repr(err)}'
            )
            Logger.log_error(self.error_respons)
            return False

    def __validate_open_close_order(self) -> bool:
        """Validate the order of the open/close items for the
        whole week. A day ending with an 'open' item can not be followed by
        an empty list for the next day, since an empty list indicates a
        closed day.
        """

        # Sort the entries per day chronologically.
        self.sorted_json_object: MainObjectType = {
            day: sorted(
                self.json_object[day],
                key=lambda x: x['value']
            )
            for day in self.ordered_days
        }

        for day, previous_day in zip(
                self.ordered_days_last_day_shifted, self.ordered_days):
            if not self.sorted_json_object[day] \
                    and self.sorted_json_object[previous_day] \
                    and self.sorted_json_object[previous_day][-1]['type'] == \
                    'open':
                self.error_respons = (
                    'A type -open- is found at the end of the day, '
                    'followed by an empty list for the next day, '
                    'implicating a closed day. We are missing an '
                    'explicit -close- type.'
                )
                Logger.log_error(self.error_respons)
                return False

        # The open-close items ordered chronologically for the whole
        # week should have alternating values (inclusive the last
        # item for the week and the first item for the week).
        open_close_alternating_list: List[str] = [
            item['type']
            for day in self.ordered_days
            for item in self.sorted_json_object[day]
        ]
        if not open_close_alternating_list:
            return True
        if (nr_open_close_items := len(open_close_alternating_list)) % 2 != 0:
            self.error_respons = (
                f'There is a missing open/close entry. '
                f'{nr_open_close_items} item(s) found, but should be an '
                f'even amount.'
            )
            Logger.log_error(self.error_respons)
            return False
        if any(i == j for i, j in zip(
            open_close_alternating_list,
            open_close_alternating_list[1:] + open_close_alternating_list[:1])
        ):
            self.error_respons = (
                'Two chronologically consecutive equal type values '
                '(open/open or close/close) found.'
            )
            Logger.log_error(self.error_respons)
            return False

        return True

    def __convert_unix_to_am_pm(
            self, unix_seconds: int, item_type: str) -> str:
        # Converts a UNIX time into a 12hour clock format.
        tail = ' - ' if item_type == 'open' else ', '
        time_format = '%I %p' if unix_seconds % 3600 == 0 \
            else '%I:%M %p'

        return strftime(
            time_format,
            gmtime(unix_seconds)
        ).lstrip('0') + tail

    def __opening_hours_per_day(
            self,
            day_items: DayElementType) -> str:
        # For one specific day, return a human readable string of the
        # open and close times.
        return 'Closed' if not day_items else ''.join(
            self.__convert_unix_to_am_pm(item['value'], item['type'])
            for item in day_items
        ).rstrip(', ')

    def __organize_day_items_for_output(self) -> MainObjectType:
        # If the day starts with a 'close' item, shift the item to
        # the end of the previous day (If on Monday, add it to
        # the end of Sunday).
        reset_days = self.sorted_json_object.copy()
        for day, previous_day in zip(
            self.ordered_days_last_day_shifted, self.ordered_days
        ):
            if reset_days[day] and reset_days[day][0]['type'] == 'close':
                reset_days[previous_day].append(reset_days[day].pop(0))

        return reset_days

    def __client_browser(self) -> bool:
        # Derive if the client is a browser. This will determine how a
        # newline should be encoded ('<br \>' vs '\n'). The derivation is
        # based on the presence of a known rendering engine in the header
        # 'User-Agent'.
        if self.header_value_user_agent and any(
            rendering_engine in self.header_value_user_agent
            for rendering_engine in self.rendering_engines
        ):
            return True
        return False

    def __output_format_in_json(self) -> bool:
        # Derive if output should be in plain text or json based on the
        # POST request (which has priority) and the 'Accept' header request
        if self.post_value_format_of_output == 'json':
            return True
        if not self.post_value_format_of_output and \
                self.header_value_accept == 'application/json':
            return True
        return False

    def __format_output(self) -> str:
        # The string with the open and closing times is created
        reset_days = self.__organize_day_items_for_output()
        if self.client_is_browser and not self.json_out:
            newline = '<br />'
        else:
            newline = '\n'

        return(''.join(
            item
            for item in [
                f'{day.capitalize()}: '
                f'{self.__opening_hours_per_day(reset_days[day])}'
                f'{newline}'
                for day in self.ordered_days
            ]
        ))

    def output_schedule(self) -> str:
        if self.__validate_input():
            if self.json_out:
                return json.dumps({'data': self.__format_output()})
            else:
                return self.__format_output()
        else:
            if self.json_out:
                return json.dumps({'error': self.error_respons})
            else:
                return self.error_respons + '\n'
