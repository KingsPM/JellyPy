import requests
import json
import pprint as pp


def close_case(_irvn, token):

    """
    :param _irvn: IR & version number. Format is ir-vn
    :param token: JWT token
    :return: json response from flask API. If CR post is successful, it returns the clinical report in JSON format,
    otherwise it returns reason for error
    """

    # Header info:
    # testing_on (optional, default=False): whether to use the beta CPI API
    # x-passtoken-cipapi (required): API token to pass for authentication
    # reportingDate (optional, default=today's date): date of clinical report

    url = 'http://localhost:5000/api/close_case/'

    headers = {'content-type': 'application/json',
               'x-passtoken-cipapi': token
               }

    data = {'testing_on': True,
            'reportingDate': '2019-07-01'}

    payload = json.dumps(data)
    r = requests.post(url + _irvn, headers=headers, data=payload)
    return r.json()


if __name__ == '__main__':

    _irvn = '\d{2}-\d{1}'
    token = '<JWT token>'

    pp.pprint(close_case(_irvn, token))
