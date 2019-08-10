import adal
import flask
import uuid
import requests
import config
from flask import redirect,request
app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'development'

# PORT = 5000  # A flask app by default runs on PORT 5000
# AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
# REDIRECT_URI = 'http://localhost:{}/getAToken'.format(PORT)
# TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
#                       'response_type=code&client_id={}&redirect_uri={}&' +
#                       'state={}&resource={}')


# @app.route("/")
# def main():
#     login_url = 'http://localhost:{}/login'.format(PORT)
#     resp = flask.Response(status=307)
#     resp.headers['location'] = login_url
#     return resp


# @app.route("/login")
# def login():
#     auth_state = str(uuid.uuid4())
#     flask.session['state'] = auth_state
#     authorization_url = TEMPLATE_AUTHZ_URL.format(
#         config.TENANT,
#         config.CLIENT_ID,
#         REDIRECT_URI,
#         auth_state,
#         config.RESOURCE)
#     resp = flask.Response(status=307)
#     resp.headers['location'] = authorization_url
#     print('resp is')
#     print(resp)
#     return resp
@app.route("/shobhit",methods = ['POST', 'GET'])
def shobhit():
    data = request.form.to_dict()
    print(data['id_token'])
    # print(request.form)
    return 'hello'


@app.route("/ext")
def ext():
    
    # print(data['id_token'])
    return redirect("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/oauth2/authorize?response_type=id_token%20code&client_id=c80344c2-d7fc-41e1-adcc-dd33683a7f6b&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fshobhit&state=c0756113-6172-47f2-8afc-666f315c15b1&client-request-id=0de0f9e0-a2f4-4853-9bd2-7326f1f409d1&x-client-SKU=Js&x-client-Ver=1.0.17&nonce=3f993c47-3042-4669-bdce-02024f6c802f&response_mode=form_post")
    # return redirect("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/oauth2/v2.0/authorize?client_id=c62087b9-cfed-4105-a9c2-4fd3953ceed5&response_type=id_token&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fshobhit&response_mode=fragment&scope=openid&state=12345&nonce=678910")


# @app.route("/getAToken")
# def main_logic():
#     code = flask.request.args['code']
#     state = flask.request.args['state']
#     if state != flask.session['state']:
#         raise ValueError("State does not match")
#     auth_context = adal.AuthenticationContext(AUTHORITY_URL)
#     token_response = auth_context.acquire_token_with_authorization_code(code, REDIRECT_URI, config.RESOURCE,
#                                                                         config.CLIENT_ID, config.CLIENT_SECRET)
#     # It is recommended to save this to a database when using a production app.
#     print('token is:')
#     print(token_response['accessToken'])
#     flask.session['access_token'] = token_response['accessToken']

#     return flask.redirect('/graphcall')


# @app.route('/graphcall')
# def graphcall():
#     if 'access_token' not in flask.session:
#         return flask.redirect(flask.url_for('login'))
#     endpoint = config.RESOURCE + '/' + config.API_VERSION + '/me/'
#     http_headers = {'Authorization': 'Bearer ' + flask.session.get('access_token'),
#                     'User-Agent': 'adal-python-sample',
#                     'Accept': 'application/json',
#                     'Content-Type': 'application/json',
#                     'client-request-id': str(uuid.uuid4())}
#     graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
#     return flask.render_template('display_graph_info.html', graph_data=graph_data)


if __name__ == "__main__":
    app.run()
