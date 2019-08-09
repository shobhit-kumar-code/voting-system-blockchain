import adal
import swagger_client
from swagger_client.api_client import ApiClient
context = adal.AuthenticationContext("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/",api_version=None)
client_id="c62087b9-cfed-4105-a9c2-4fd3953ceed5"
client_secret="QUwt[:X:pKVQkFevjb0vLndwnzrH34.7"
res='c80344c2-d7fc-41e1-adcc-dd33683a7f6b'
token = context.acquire_token_with_username_password(resource='https://graph.windows.net',username="shobhit@kumarshobhit98outlook.onmicrosoft.com",password="Alonso123",client_id=client_id)
# print(token['accessToken'])
# token = context.acquire_token_with_client_credentials(client_id,client_id,client_secret)
# api_client = ApiClient()
# bearer_token = "Bearer "+token['accessToken']
# print(bearer_token)
# print(token.keys())
print(token['accessToken'])
# api_client.set_default_header('Authorization',bearer_token)
# api_user = swagger_client.UsersApi(api_client)
# me = api_user.me_get()
# pprint(me)