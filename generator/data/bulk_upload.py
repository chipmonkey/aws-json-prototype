""" Upload multiple JSON files to an AWS (or any) JSON API
Equivalent to:

curl -v -X POST \
'https://j7lpala7eb.execute-api.us-east-1.amazonaws.com/lambda' \
-H 'content-type: application/json' \
--data-binary "@file"

"""
import os
import requests

URL = 'https://j7lpala7eb.execute-api.us-east-1.amazonaws.com/lambda'
HEADERS = {'content-type': 'application/json'}
SOURCE_DIR = 'processed'


def upload_files():
    """ Upload ALL the files
    """
    directory = '.' + os.sep + SOURCE_DIR + os.sep

    for filename in os.listdir(directory):
        print(f'processing {directory + filename}')
        result = requests.post(URL,
                               data=open(directory + filename, 'r'),
                               headers=HEADERS)
        print(f'result: {result.text}')


if __name__ == '__main__':
    upload_files()
