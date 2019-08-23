from pyCIPAPI.cva import get_cva_service_status, get_cva_auth_token, get_cva_case
import pprint as pp

token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwZGF2aWRzb24xIiwiZ3JvdXBzIjpbImRsX3Jlc3VsdHNfcmVwb3J0aW5nIiwiYmlvLWN2YS1yZWFkX2Nhc2VzIiwiYmlvLWN2YS1yZWFkX2FnZ3JlZ2F0aW9ucyJdLCJpYXQiOjE1NjU5NjYxNTUsImV4cCI6MTU2ODM4NTM1NX0.mmM8cw75AStEtjmyMceoTn5lb_Vt2tqGMaSqDtugM_o'
#token = 'fdgdfg.dgdf.gd'
# Get CVA service status
#pp.pprint(get_cva_service_status(api_version=0))


# Return JWT token
print(get_cva_auth_token())

# Get Case ID
case_id = '1002-1'
print(get_cva_case(case_id, token=token))

