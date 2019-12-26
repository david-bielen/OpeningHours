# -*- coding: utf-8 -*-

"""
A flask app that re-formats the weekly opening hours of a restaurant into a
humand readable format. It accepts a get request on '/' and a post request
on '/api'. The get request returns an HTML form, which posts to '/api'.  In
the response to the post request, we validate the input and return output as
a JSON string or a web appropriate format.
"""

from flask import Flask
from static.static_variables import (
    static_schema, static_ordered_days, rendering_engines
)
from common.requestdata import RequestData
from common.logger import Logger
from common.openinghours import OpeningHours


#############
# FLASK APP #
#############

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home() -> str:
    json_string = '{"monday" : [], "tuesday" : [{"type" : "open", \
    "value" : 36000},{"type" : "close", "value" : 64800}], "wednesday" : [],\
    "thursday" : [{"type" : "open", "value" : 36000}, {"type" :"close" \
    ,"value" : 64800}], "friday" : [{"type" : "open", "value" : 36000}], \
    "saturday" : [{"type" : "close", "value": 3600 }, {"type" : "open", \
    "value" : 36000}], "sunday" : [{"type" : "close", "value" : 3600}, \
    {"type" : "open", "value" : 43200}, {"type" : "close", "value" : \
    75600}]}'

    return """<body style="max-width:40rem;margin:auto;margin-top:5rem;">
    <form action="/api" method="POST" id="form_id">
        <label for="json_data">Input JSON data:</label><br><br>
        <textarea name="json_data" id="a" rows="20" cols="60"
        autofocus style="font-size:1rem;"></textarea><br><br>
        <input type="radio" name="format_of_output" value="text">
        Output in plain text<br>
        <input type="radio" name="format_of_output" value="json">
        Output in JSON<br>
    </form>
    <button
        style="font-size:1rem;"
        onclick="document.getElementById('form_id').submit();"
    >Submit</button>
    <br><br><br><br>
    Example input:
    <button
        onclick="document.getElementById('a').value =
        document.getElementById('b').innerHTML"
        style="font-size:1rem;margin-left:2rem;"
    >Copy</button>
    <pre id="b" style="max-width:28rem; word-wrap:break-word; white-space:
    pre-wrap; background:#eee; padding:1rem;">{0}</pre>
    """.format(json_string.replace(' ', ''))


@app.route('/api', methods=['POST'])
def api() -> str:
    if RequestData.get_data():
        restaurant_schedule = OpeningHours(
            RequestData.get_data(),
            RequestData.output_format_in_json(),
            static_schema,
            static_ordered_days,
            RequestData.client_is_browser(rendering_engines)
        )
        return restaurant_schedule.output_schedule()
    else:
        Logger.log_warning('No data found.\n')
        return 'No data found.\n'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
