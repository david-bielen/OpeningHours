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
<br/><br/>

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
<br/><br/>

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
<br/><br/>

* Example 3 ('format_of_output=json' as POST parameter):
```console
curl --data 'json_data={"monday":[],"tuesday":[{"type":"open","value":36000},{"type":"close","value":64800}],"wednesday":[],"thursday":[{"type":"open","value":36000},{"type":"close","value":64800}],"friday":[{"type":"open","value":36000}],"saturday":[{"type":"close","value":3600},{"type":"open","value":36000}],"sunday":[{"type":"close","value":3600},{"type":"open","value":43200},{"type":"close","value":75600}]}&format_of_output=json' http://127.0.0.1:8080/api
```

  **Output:**<br/>
{"data": "Monday: Closed\nTuesday: 10 AM - 6 PM\nWednesday: Closed\nThursday: 10 AM - 6 PM\nFriday: 10 AM - 1 AM\nSaturday: 10 AM - 1 AM\nSunday: 12 PM - 9 PM\n"}<br/>
<br/><br/>

* Example 4 ('Accept: application/json' in header):
```console
curl --header 'Accept: application/json'  --data 'json_data={"monday":[],"tuesday":[{"type":"open","value":36000},{"type":"close","value":64800}],"wednesday":[],"thursday":[{"type":"open","value":36000},{"type":"close","value":64800}],"friday":[{"type":"open","value":36000}],"saturday":[{"type":"close","value":3600},{"type":"open","value":36000}],"sunday":[{"type":"close","value":3600},{"type":"open","value":43200},{"type":"close","value":75600}]}' http://127.0.0.1:8080/api
```

  **Output:**<br/>
{"data": "Monday: Closed\nTuesday: 10 AM - 6 PM\nWednesday: Closed\nThursday: 10 AM - 6 PM\nFriday: 10 AM - 1 AM\nSaturday: 10 AM - 1 AM\nSunday: 12 PM - 9 PM\n"}<br/>
<br/><br/>

* Example 5 (non-compatible JSON)
```console
curl --data 'json_data={"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[],"mayday":[]}' http://127.0.0.1:8080/api
```

  **Output:**<br/>
Invalid schema: 'sunday' is a required property<br/>
<br/><br/>

* Example 6 (non-compatible JSON, with 'format_of_output=json' as POST parameter)
```console
curl --data 'json_data={"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[],"mayday":[]}&format_of_output=json' http://127.0.0.1:8080/api
```

  **Output:**<br/>
{"error": "Invalid schema: 'sunday' is a required property\n"}<br/>
<br/><br/>

## Thoughts about the JSON Format.

Special case 1 states that "If a restaurant is closed the whole day, an array of opening hours is empty". Which is not the same as saying "If an empty array of opening hours is present, the restaurant is closed the whole day". But the example to showcase this special case indicates otherwise: " “tuesday”: [] means a restaurant is closed on Tuesdays". If we can interprete special case 1 as "if an empty array is present, the restaurant is closed all day", then there is the following problem:
A restaurant that opens on Friday 8 PM, is open the whole day of Saturday, and closes on Sunday 06 AM, can not be encoded with the current JSON format.

The following input would be invalid:<br/>
```javascript
{
  "monday": [],
  "tuesday": [],
  "wednesday": [],
  "thursday": [],
  "friday": [
    {
      "type": "open",
      "value": 72000
    }
  ],
  "saturday": [],
  "sunday": [
    {
      "type": "close",
      "value": 21600
    }
  ]
}
```
<br/><br/>
To avoid the above issue, a vectorized approach can be used. We only encode the opening hours (in UNIX time, as above), and the duration of the open state of the restaurant, in minutes. This has the added benefit of a more concise encoding of opening hours.
<br/>
```javascript
{
  "monday": [],
  "tuesday": [],
  "wednesday": [],
  "thursday": [],
  "friday": [
    {
      "open": 72000,
      "duration": 2040
    }
  ],
  "saturday": [],
  "sunday": []
}
```
  **Output:**<br/>
Monday: Closed<br/>
Tuesday: Closed<br/>
Wednesday: Closed<br/>
Thursday: Closed<br/>
Friday: 20:00 - 24:00<br/>
Saturday: 00:00 - 24:00<br/>
Sunday: 00:00 - 06:00<br/>
.


