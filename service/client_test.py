import requests, json, datetime, jwt

CIP_API_SERVER_URL = 'https://cipapi-beta.genomicsengland.co.uk/api/2/'
expired_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBkYXZpZHNvbjEiLCJvcmlnX2lhdCI6MTU2MjA1NTE1NSwidXNlcl9pZCI6NzIsImVtYWlsIjoicGhpbGlwLmRhdmlkc29uMkBuaHMubmV0IiwiZXhwIjoxNTYyMDczMTU1fQ.EX49uPGXw47SwrGRKWB_6t31iCqdc8fmGOI5c2IRots'


def get_authenticated_header(CIP_API_SERVER_URL):

    auth_endpoint = "get-token/"

    irl_response = requests.post(
        url = CIP_API_SERVER_URL + auth_endpoint,
        json=dict(
            username='pdavidson1',
            password='AqEP6KEtK',
        ),
    )

    irl_response_json = irl_response.json()

    token = irl_response_json.get('token')
    return token

# token = get_authenticated_header(CIP_API_SERVER_URL)
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBkYXZpZHNvbjEiLCJvcmlnX2lhdCI6MTU2MjA4MTQ4NiwidXNlcl9pZCI6NzIsImVtYWlsIjoicGhpbGlwLmRhdmlkc29uMkBuaHMubmV0IiwiZXhwIjoxNTYyMDk5NDg2fQ.9SA20fC7TNBgO2o4yo8or4vgPTP0ilVgJk-SfCNdExQ'


def close_case(_irvn, token):

    url = 'http://localhost:5000/api/close_case/'

    headers={'content-type': 'application/json',
             'auth_token': token
             }

    data={'testing_on': 'true',
          'reportingDate': '2019-07-01'}

    payload = json.dumps(data)

    r = requests.post(url + _irvn, headers=headers, data=payload)

    return r.json()

print(close_case('79-1', token))