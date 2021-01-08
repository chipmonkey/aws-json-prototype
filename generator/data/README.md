Manual scripts to transform sample data.

Requires synthea\_sample\_data\_fhir\_dstu2\_sep2019.zip
Unzip that file to its natural subfolder.

cache\_nominatim\_dstu2.py will iterate over the files,
call the OpenStreetMap Nominatim API,
and cache the results in dstu2\_cache.db

This is an overly conservative approach so that we're kind to the OSM API rate limits.

The python process exhibits how first\_name and last\_name can be retrieved; but
right now this is not committed to SQLite.  What IS committed is the raw JSON response
(if any) from OpenStreetMaps.  Mostly we'll need this to pull zip\_code, which
is not provided in the raw JSON data.
