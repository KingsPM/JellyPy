from .auth import AuthenticatedCIPAPISession
from .config import live_100k_base_url, beta_testing_base_url


def get_cip_service_status(testing_on=False, api_version=2):
    """ [TODO: Description]

    Args:
        [TODO: Arguments]
    """
    s = AuthenticatedCIPAPISession(testing_on=testing_on, api_version=api_version)

    if testing_on:
        base_url = beta_testing_base_url
    else:
        base_url = live_100k_base_url

    url = '{base_url}{api_version}/health'.format(base_url=base_url, api_version=api_version)

    r = s.get(url)

    return r.json()


def get_cip_auth_token(testing_on=False, api_version=2):
    """ [TODO: Description]

    Args:
        [TODO: Arguments]
    """

    s = AuthenticatedCIPAPISession(testing_on=testing_on, api_version=api_version)

    return s.headers['Authorization'].strip('Bearer ')
