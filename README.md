# OpeningHours
A program that takes JSON-formatted opening hours of a restaurant as an input and outputs hours in a more human readable format.


## How to use
You will need python 3.8 or higher.


### Browser
In a terminal, run:
```console
python flask_app.py
```
Open the URL (http://127.0.0.1:8080/) in the browser.


### Terminal
run:
```console
python flask_app.py
```
In a second terminal window, make a POST request with curl to http://127.0.0.1:8080/api. Provide the json data with the paramater 'json_data', and (optional) provide the output format either with a 'format_of_output=json' POST parameter, or with the 'Accept' header request 'application/json'.

A few examples:
* Example 1:
```console
curl --data 'json_data={"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[],"sunday":[]}' http://127.0.0.1:8080/api
```

**Output:**<br/>
Monday: Closed<br/>
Tuesday: Closed<br/>
Wednesday: Closed<br/>
Thursday: Closed<br/>
Friday: Closed<br/>
Saturday: Closed<br/>
Sunday: Closed<br/>

* Example 2:
```console
curl --data 'json_data={"monday":[],"tuesday":[{"type":"open","value":36000},{"type":"close","value":64800}],"wednesday":[],"thursday":[{"type":"open","value":36000},{"type":"close","value":64800}],"friday":[{"type":"open","value":36000}],"saturday":[{"type":"close","value":3600},{"type":"open","value":36000}],"sunday":[{"type":"close","value":3600},{"type":"open","value":43200},{"type":"close","value":75600}]}' http://127.0.0.1:8080/api
```

**Output:**<br/>
Monday: Closed<br/>
Tuesday: 10 AM - 6 PM<br/>
Wednesday: Closed<br/>
Thursday: 10 AM - 6 PM<br/>
Friday: 10 AM - 1 AM<br/>
Saturday: 10 AM - 1 AM<br/>
Sunday: 12 PM - 9 PM<br/>

* Example 3 ('format_of_output=json' as POST parameter):
```console
curl --data 'json_data={"monday":[],"tuesday":[{"type":"open","value":36000},{"type":"close","value":64800}],"wednesday":[],"thursday":[{"type":"open","value":36000},{"type":"close","value":64800}],"friday":[{"type":"open","value":36000}],"saturday":[{"type":"close","value":3600},{"type":"open","value":36000}],"sunday":[{"type":"close","value":3600},{"type":"open","value":43200},{"type":"close","value":75600}]}&format_of_output=json' http://127.0.0.1:8080/api
```

**Output:**<br/>
{"data": "Monday: Closed\nTuesday: 10 AM - 6 PM\nWednesday: Closed\nThursday: 10 AM - 6 PM\nFriday: 10 AM - 1 AM\nSaturday: 10 AM - 1 AM\nSunday: 12 PM - 9 PM\n"}<br/>

* Example 4 ('Accept: application/json' in header):
```console
curl --header 'Accept: application/json'  --data 'json_data={"monday":[],"tuesday":[{"type":"open","value":36000},{"type":"close","value":64800}],"wednesday":[],"thursday":[{"type":"open","value":36000},{"type":"close","value":64800}],"friday":[{"type":"open","value":36000}],"saturday":[{"type":"close","value":3600},{"type":"open","value":36000}],"sunday":[{"type":"close","value":3600},{"type":"open","value":43200},{"type":"close","value":75600}]}' http://127.0.0.1:8080/api
```

**Output:**<br/>
{"data": "Monday: Closed\nTuesday: 10 AM - 6 PM\nWednesday: Closed\nThursday: 10 AM - 6 PM\nFriday: 10 AM - 1 AM\nSaturday: 10 AM - 1 AM\nSunday: 12 PM - 9 PM\n"}<br/>

* Example 5 (non-compatible JSON)
```console
curl --data 'json_data={"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[],"mayday":[]}' http://127.0.0.1:8080/api
```

**Output:**<br/>
Invalid schema: 'sunday' is a required property