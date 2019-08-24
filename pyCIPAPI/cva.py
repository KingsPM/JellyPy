from .auth import AuthenticatedCVASession
from .config import cva_base_url


def get_cva_service_status(api_version=0):
    """ [TODO: Description]

    Args:
        [TODO: Arguments]
    """
    s = AuthenticatedCVASession(api_version=api_version)
    
    url = '{base_url}{api_version}/system-status'.format(base_url=cva_base_url, api_version=api_version)

    r = s.get(url)

    return r.json()


def get_cva_auth_token(api_version=0):
    """ [TODO: Description]

    Args:
        [TODO: Arguments]
    """

    s = AuthenticatedCVASession(api_version=api_version)

    return s.headers['Authorization'].strip('Bearer ')


def get_cva_case(case_id, api_version=0, token=None):
    """ [TODO: Description]

    Args:
        [TODO: Arguments]
    """

    s = AuthenticatedCVASession(api_version=api_version, token=token)

    search_url = '{base_url}{api_version}/cases/{case_id}'.format(base_url=cva_base_url, 
                                                                  api_version=api_version,
                                                                  case_id=case_id)

    r = s.get(search_url)

    return r.json()
