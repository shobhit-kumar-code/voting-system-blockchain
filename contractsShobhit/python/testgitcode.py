from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# create an instance of the API class
api_instance = swagger_client.ApplicationsApi()
application_id = 'c80344c2-d7fc-41e1-adcc-dd33683a7f6b' # str | The id of the application.

try:
    # 
    api_instance.application_delete(application_id)
except ApiException as e:
    print("Exception when calling ApplicationsApi->application_delete: %s\n" % e)