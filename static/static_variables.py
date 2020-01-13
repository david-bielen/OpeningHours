# -*- coding: utf-8 -*-

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
    "maxProperties": len(static_ordered_days)
}

# rendering engines
rendering_engines = ['Gecko', 'WebKit', 'Presto', 'Trident']
