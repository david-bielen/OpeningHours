# -*- coding: utf-8 -*-

from time import gmtime
import json
import jsonschema  # type: ignore
from typing import Dict, List, Union, Optional
from time import strftime
from common.logger import Logger
from static.static_variables import (
    static_schema, static_ordered_days, MainObjectType, DayElementType,
    rendering_engines
)


class OpeningHours:
    """A class that validates JSON input representing the opening hours
    of a restaurant, and encodes the input into a humand readable format
    of the opening hours, formatted using 12-hour clock.
    """

    def __init__(
        self,
        input_string: str,
        json_output: bool,
        schema: object,
        ordered_days: list,
        is_browser: bool
    ) -> None:
        self.input_string: str = input_string
        self.json_output: bool = json_output
        self.schema: object = schema
        self.ordered_days: List[str] = ordered_days
        self.ordered_days_last_day_shifted: List[str] = ordered_days[1:] \
            + ordered_days[:1]
        self.is_browser: bool = is_browser
        self.error_respons: str

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
            self.json_object: Dict = json.loads(self.input_string)
            return True
        except json.decoder.JSONDecodeError as err:
            self.error_respons = \
                f'Input is not valid JSON. {repr(err)}\n'
            Logger.log_error(self.error_respons)
            return False
        except Exception as err:
            self.error_respons = (
                f'Non-defined exception while validating JSON: '
                f'{repr(err)}\n'
            )
            Logger.log_error(self.error_respons)
            return False

    def __validate_schema(self) -> bool:
        """Verify if the json object adheres to our schema."""
        try:
            jsonschema.validate(self.json_object, self.schema)
            return True
        except jsonschema.ValidationError as err:
            self.error_respons = (f'Invalid schema: {err.message}\n')
            Logger.log_error(self.error_respons)
            return False
        except Exception as err:
            self.error_respons = (
                f'Undefined exception while validating schema: '
                f'{repr(err)}\n'
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
                    'explicit -close- type.\n'
                )
                Logger.log_error(self.error_respons)
                return False

        # The open-close items ordered chronologically for the whole
        # week should have alternating values (inclusive the last
        # item for the week and the first item for the week).
        open_close_alternating_list: list = [
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
                f'even amount.\n'
            )
            Logger.log_error(self.error_respons)
            return False
        if any(i == j for i, j in zip(
            open_close_alternating_list,
            open_close_alternating_list[1:] + open_close_alternating_list[:1])
        ):
            self.error_respons = (
                'Two chronologically consecutive equal type values '
                '(open/open or close/close) found.\n'
            )
            Logger.log_error(self.error_respons)
            return False

        return True

    def __convert_unix_to_am_pm(
            self, unix_seconds: int, item_type: str) -> str:
        # Converts a UNIX time into a 12hour clock format.
        tail: str = ' - ' if item_type == 'open' else ', '
        time_format: str = '%I %p' if unix_seconds % 3600 == 0 \
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

    def __organize_day_items_for_print(self) -> MainObjectType:
        # If the day starts with a 'close' item, shift the item to
        # the end of the previous day (If on Monday, add it to
        # the end of Sunday).
        reset_days: MainObjectType = self.sorted_json_object.copy()
        for day, previous_day in zip(
            self.ordered_days_last_day_shifted, self.ordered_days
        ):
            if reset_days[day] and reset_days[day][0]['type'] == 'close':
                reset_days[previous_day].append(reset_days[day].pop(0))

        return reset_days

    def __format_hours_output(self) -> str:
        # The string with the open and closing times is created
        reset_days: MainObjectType = self.__organize_day_items_for_print()
        if self.is_browser and not self.json_output:
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
            if self.json_output:
                if self.is_browser:
                    return json.dumps(
                        {
                            'data': self.__format_hours_output()
                        }
                    )
                else:
                    return json.dumps(
                        {
                            'data': self.__format_hours_output()
                        }
                    ) + '\n'
            else:
                return self.__format_hours_output()
        else:
            if self.json_output:
                return json.dumps(
                    {
                        'error': self.error_respons
                    }
                )
            else:
                return self.error_respons
