# -*- coding: utf-8 -*-

from typing import Dict, List, TypeVar

# The order of the days, starting with Monday.
static_ordered_days = [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
    'saturday', 'sunday']

# Schema to be used in jsonschema.
static_schema = {
    "type": "object",
    "additionalProperties": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["open", "close"]
                },
                "value": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 86399
                }
            },
            "required": ["type", "value"],
            "maxProperties": 2
        }
    },
    "required": static_ordered_days,
    "maxProperties": 7
}

# rendering engines
rendering_engines = ['Gecko', 'WebKit', 'Presto', 'Trident', 'Trident']

# Type aliases
SI = TypeVar('SI', str, int)
DayElementType = List[Dict[str, SI]]
MainObjectType = Dict[str, DayElementType]
