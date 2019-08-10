import json
sample_parameters = json.loads('{"resource": "00000002-0000-0000-c000-000000000000","tenant" : "rrandallaad1.onmicrosoft.com","authorityHostUrl" : "https://login.microsoftonline.com","clientId" : "624ac9bd-4c1c-4687-aec8-b56a8991cfb3","username" : "user1","password" : "verySecurePassword"}')
print(sample_parameters)

GRAPH_RESOURCE = '00000002-0000-0000-c000-000000000000'
RESOURCE = sample_parameters.get('resource', GRAPH_RESOURCE)
print(RESOURCE)