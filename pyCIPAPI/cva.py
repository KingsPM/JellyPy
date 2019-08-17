from .auth import AuthenticatedCVASession

def get_service_status():

    s = AuthenticatedCVASession()
    
    url = 'https://cva.genomicsengland.nhs.uk/cva/api/0/system-status'

    r = s.get(url)

    return r.json()

def get_auth_token(auth_credentials):

    s = AuthenticatedCVASession(auth_credentials=auth_credentials)

    return s.headers['Authorization']

def get_case(case_id, token=None):

    s = AuthenticatedCVASession(token=token)

    url = 'https://cva.genomicsengland.nhs.uk/cva/api/0/cases/{case_id}'.format(case_id=case_id)

    r = s.get(url)

    return r.json()
