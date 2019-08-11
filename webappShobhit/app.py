import adal
import flask
import uuid
import urllib
import requests
import config
import json
from flask import redirect,request,render_template
app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'development'
session={}
applid=4
candidateRoleId=7
voteWorkflowPropertyId=7
currentuserid=-1
def getyourroleid():
    global currentuserid
    url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/applications/"+str(applid)+"/roleAssignments"
    # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
    headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json',
    
    responsefromapi = requests.get(url,headers=headers)
    print(responsefromapi.url)
    print(responsefromapi.status_code)
    print(responsefromapi.json())
    if responsefromapi.status_code == 200:
        results=json.loads(responsefromapi.content.decode('utf-8'))
        print('user role code is')
        x=0
        while results['roleAssignments'][x]['user']['userID']!=currentuserid:
            print(results['roleAssignments'][x]['user']['userID'])
            print(currentuserid)
            x=x+1
        print(results['roleAssignments'][x]['applicationRoleId'])
        if results['roleAssignments'][x]['applicationRoleId']==candidateRoleId:
            return 'candidate'
        else:
            return 'voter'

def getusertype():
    global currentuserid
    url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/users/me"
    # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
    headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json',
    
    responsefromapi = requests.get(url,headers=headers)
    print(responsefromapi.url)
    print(responsefromapi.status_code)
    print(responsefromapi.json())
    if responsefromapi.status_code == 200:
        results=json.loads(responsefromapi.content.decode('utf-8'))
        print('hello')
        print(results['currentUser']['userID'])
        currentuserid=results['currentUser']['userID']
        if results['capabilities']['canUpgradeWorkbench']==True:
            return 'admin'
        else:
            
            return 'user'
        
    else:
        return 'failed at getting user type'

@app.route("/shobhit",methods = ['POST', 'GET'])
def shobhit():
    
    data = request.form.to_dict()
    print(data['id_token'])
    auth_token=data['id_token']
    session['auth_token']=auth_token
    usertype = getusertype()
    if usertype=='user':
        usertype1=getyourroleid()
        if usertype1=='voter':
            return render_template('home.html')
        else:
            return render_template('candidatehome.html')
    else:
        return render_template('adminhome.html')
@app.route("/launchcandidate",methods = ['POST', 'GET'])
def launchcandidate():
    return 'tolaunchcandidate'
@app.route("/reguser",methods = ['POST', 'GET'])
def reguser():
    # candidate_uid=request.form['uid']
    #add this UID to Mongodb for thr candidate, and verify it is unique, if not send back to /ext
    #all this comes from adminhome.html

    apidata={
        "externalID": request.form['externalid'],
        "firstName": request.form['firstname'],
        "lastName": request.form['lastname'],
        "emailAddress": request.form['emailid']
      }
    print(apidata)
    url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/users"
    # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
    headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json',
    
    responsefromapi = requests.post(url,json=apidata,headers=headers)
    print(responsefromapi.url)
    print(responsefromapi.status_code)
    if responsefromapi.status_code == 200:
        results=json.loads(responsefromapi.content.decode('utf-8'))
        newuser=results

        apidata={
            "userId": newuser,
            "applicationRoleId": 7 #role for candidate
          }
        print(apidata)
        url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/applications/"+str(applid)+"/roleAssignments"
        # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
        headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}

        responsefromapitoassignrole = requests.post(url,json=apidata,headers=headers)

        return 'thanks for voting'
    else:
        return 'failed'


@app.route("/voted",methods = ['POST', 'GET'])
def voted():
    candidate_uid=request.form['uid']


    apidata={"workflowFunctionID": 9,"workflowActionParameters": []}
    url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/contracts/"+str(candidate_uid)+"/actions"
    # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
    headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json',
    
    responsefromapi = requests.post(url,json=apidata,headers=headers)
    print(responsefromapi.url)
    print(responsefromapi.status_code)
    if responsefromapi.status_code == 200:
        results=json.loads(responsefromapi.content.decode('utf-8'))
        return 'thanks for voting'
    else:
        return 'failed'

    return 'thanks for voting'

@app.route("/shobhit1",methods = ['POST', 'GET'])
def shobhit1():
    data = request.form.to_dict()
    print(data['id_token'])
    # print(request.form)

    apidata={"workflowFunctionID": 1,"workflowActionParameters": [  { "name": "message", "value": "lalala", "workflowFunctionParameterId": 3 } ] }
    auth_token=data['id_token']
    url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/contracts"
    params={'workflowId':1,'contractCodeId':1,'connectionId':1}
    headers={'Authorization': 'Bearer {0}'.format(auth_token)}#{'Content-Type': 'application/json',
    
    responsefromapi = requests.post(url,params=params, json=apidata,headers=headers)
    print(responsefromapi.url)
    print(responsefromapi.status_code)
    if responsefromapi.status_code == 200:
        newid=json.loads(responsefromapi.content.decode('utf-8'))
        return 'a'
    else:
        return 'hello'

    return 'hello'


@app.route("/ext")
def ext():    
    # print(data['id_token'])
    return redirect("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/oauth2/authorize?response_type=id_token%20code&client_id=c80344c2-d7fc-41e1-adcc-dd33683a7f6b&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fshobhit&state=c0756113-6172-47f2-8afc-666f315c15b1&client-request-id=0de0f9e0-a2f4-4853-9bd2-7326f1f409d1&x-client-SKU=Js&x-client-Ver=1.0.17&nonce=3f993c47-3042-4669-bdce-02024f6c802f&response_mode=form_post")
    # return redirect("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/oauth2/v2.0/authorize?client_id=c62087b9-cfed-4105-a9c2-4fd3953ceed5&response_type=id_token&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fshobhit&response_mode=fragment&scope=openid&state=12345&nonce=678910")

if __name__ == "__main__":
    app.run()