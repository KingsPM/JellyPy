from pyCIPAPI.cipapi import get_cip_service_status, get_cip_auth_token
import pprint as pp

pp.pprint(get_cip_service_status(testing_on=True))

pp.pprint(get_cip_auth_token(testing_on=True))
