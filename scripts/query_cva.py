from pyCIPAPI.cva import get_service_status, get_case, get_auth_token

token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwZGF2aWRzb24xIiwiZ3JvdXBzIjpbImRsX3Jlc3VsdHNfcmVwb3J0aW5nIiwiYmlvLWN2YS1yZWFkX2Nhc2VzIiwiYmlvLWN2YS1yZWFkX2FnZ3JlZ2F0aW9ucyJdLCJpYXQiOjE1NjU5NjYxNTUsImV4cCI6MTU2ODM4NTM1NX0.mmM8cw75AStEtjmyMceoTn5lb_Vt2tqGMaSqDtugM_o'
# token = 'fdgdfgsgrsgrh'

#print(get_service_status(token=token))


#print(get_case('51029-1', token=token))

auth_credentials = {
    "username": "pdavidson1",
    "password": "AqEP6KEtK"
}

print(get_auth_token(auth_credentials=auth_credentials))