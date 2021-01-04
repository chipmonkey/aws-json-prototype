# aws-json-prototype
Chip's playground for building an AWS API Endpoint for fun and learning

# QuickStart

## SuperQuick:
Hopefully this will do it:
```
make init
make config
make deploy
```

For other available commands just use:
```
make help
```

## Requirements
* This has only been tested on Ubuntu Linux 18.04; other OSes may work but are not tested
* You will require an AWS aws\_access\_key\_id and aws\_secret\_access\_key.  Ideally these should already be installed and working.  In theory the configure script will prompt you for them if not, but honestly that isn't working yet.
* Some flavor of python3 is required.  This was tested with Python 3.8.  Virtual environments are used for all libraries.
* `awscli` and `python3-pytest` will be installed by apt (via Makefile) if they do not already exist.

## Key Decision Points
* Use Lambda ?  (yes)
* Use S3 for Raw JSON ? (yes)
* Use a messaging service to handle back end processing ? (TBD)
* Use AWS specific tools (i.e. cloudform not terraform, etc.) for learning

## In Progress:
Tracking progress in github issues - see https://github.com/chipmonkey/aws-json-prototype/issues
### Currently tracking two epics:
1. Data Handling
2. Analysis


# Resources:
## Sample Data: [via https://synthetichealth.github.io/synthea/](https://storage.googleapis.com/synthea-public/synthea_sample_data_fhir_dstu2_sep2019.zip)
