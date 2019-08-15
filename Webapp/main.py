import flask
import os
import json
from flask import Flask, render_template, request,redirect
import sys
from werkzeug import secure_filename
from vote_system import Voting
import pdb
from azurenews import NewsSearch
import cv2
import pymongo
import requests

# app.secret_key = 'development'
session={}
applid=4
candidateRoleId=7
voteWorkflowPropertyId=7
currentuserid=-1
# sys.path.append('D:\EmotionDetection')
# print(sys.path)
# from Mails import Mail
uri = "mongodb://votemadolai:RIAaSAOPHxWkFP4tfmgA0R9vz31GWMSS2Pz3S4WkwZyVAQa5gfocwAxhDijFz3g0X0EIyd0gCjcncdo8d8HsUA==@votemadolai.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
app = flask.Flask(__name__,static_url_path='/static')
fd = open("config.txt")
data = json.load(fd)


@app.route("/results")
def results():
  return flask.render_template("results.html")
@app.route("/")
def home():
    obj=NewsSearch()
    result=obj.news()
    return flask.render_template("home.html",result=result)
@app.route("/home",methods = ['POST', 'GET'])
def home_1():
    global session
    data = request.form.to_dict()
    print(data['id_token'])
    auth_token=data['id_token']
    session['auth_token']=auth_token
    obj=NewsSearch()
    result=obj.news()
    return flask.render_template("redirect_home.html",result=result)

@app.route("/list")
def list_fun():
  mapping={
    "001":"Bangalore",
    "002":"Delhi",
    "003":"Chennai",
    "004": "Mumbai",
    "005":"Kolkata",
    "006":"Hyderabad"
  }
  myclient=pymongo.MongoClient(uri)
  mydb = myclient["codefundo"]
  mycol=mydb['vote_reg']
  result=[]
  for x in mycol.find():
    result.append(x)
  return flask.render_template("electoral.html",result=result,mapping=mapping)
 
@app.route("/candidates")
def candidate_fun():
  mapping={
    "001":"Bangalore",
    "002":"Delhi",
    "003":"Chennai",
    "004": "Mumbai",
    "005":"Kolkata",
    "006":"Hyderabad"
  }
  myclient=pymongo.MongoClient(uri)
  mydb = myclient["codefundo"]
  mycol=mydb['cand_reg']
  result=[]
  for x in mycol.find():
    result.append(x)
  return flask.render_template("candidate.html",result=result,mapping=mapping)
 
@app.route("/admin_home")
def admin_home():
  obj=NewsSearch()
  result=obj.news()
  return flask.render_template("admin_home.html",result=result)
@app.route("/result_proof")
def result_proof():
  fil=open("vote_tabulate.txt","r").read()
  # import pdb; pdb.set_trace()
  entries=fil.split("\n")
  result=[]
  for e in entries:
    x,y=e.split("\t\t")
    result.append({"Name":x,"Timestamp":y})
  return flask.render_template("result_proof.html",result=result)
@app.route("/register_candidate")
def register_candidate():
    return flask.render_template("register_candidate.html")

@app.route("/register_voter")
def register_voter():
    return flask.render_template("register_voter.html")

@app.route("/register_voter_overseas")
def register_voter_overseas():
    return flask.render_template("register_voter_overseas.html")
@app.route("/register")
def register():
    return flask.render_template("home.html")

@app.route("/login")
def login():
    return flask.render_template("login.html")

@app.route("/registration_complete_candidate",methods = ['POST', 'GET'])
def registration_complete_candidate():
    mapping={
            "uid":"Unique ID",
            "fname": "First Name",
            "lname": "Last Name",
            "email": "Email ID",
            "age":"Age",
            "address":"Permanent Address",
            "gender":"Gender",
            "wardno": "Ward No",
            "photo": "Photo Upload",
            "criminal":"Criminal Records"
                      }
    if request.method=="POST":
      result=request.form
      file_handler=request.files['photo']
      #file_handler.save(os.path.join("D:\codefundo\Webapp\static\PurpleAdmin-Free-Admin-Template-master\images",secure_filename(file_handler.filename)))
      file_handler.save(os.path.join(data["ImgPath"],secure_filename(result['uid']+".jpg")))
      obj=Voting()
      # import pdb; pdb.set_trace()
      if obj.register_candidate(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],result['gender'],result['wardno'],str(file_handler.filename),result['criminal']) ==True:
          # return redirect("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/oauth2/authorize?response_type=id_token%20code&client_id=c80344c2-d7fc-41e1-adcc-dd33683a7f6b&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fregister&state=c0756113-6172-47f2-8afc-666f315c15b1&client-request-id=0de0f9e0-a2f4-4853-9bd2-7326f1f409d1&x-client-SKU=Js&x-client-Ver=1.0.17&nonce=3f993c47-3042-4669-bdce-02024f6c802f&response_mode=form_post")  
          fil=open("uid.txt","w")
          fil.write(result['uid'])
          fil.close()
          return flask.render_template("registration_complete.html",result=result,mapping=mapping,photo="../static/PurpleAdmin-Free-Admin-Template-master/images/"+file_handler.filename,visa=None,candidate=result['uid'])
      else:
        return flask.render_template("permission_denied_voter.html")
@app.route("/registration_complete_voter",methods = ['POST', 'GET'])
def registration_complete_voter():
    mapping={
        "uid":"Unique ID",
        "fname": "First Name",
        "lname": "Last Name",
        "email": "Email ID",
        "age":"Age",
        "address":"Permanent Address",
        "gender":"Gender",
        "wardno": "Ward No",
        "photo": "Photo Upload",
        "criminal":"Criminal Records"
                    }
    if request.method=="POST":
      result=request.form
      file_handler=request.files['photo']
      #file_handler.save(os.path.join("D:\codefundo\Webapp\static\PurpleAdmin-Free-Admin-Template-master\images",secure_filename(file_handler.filename)))
      file_handler.save(os.path.join(data["ImgPath"],secure_filename(result['uid']+".jpg")))

      obj=Voting()

      print(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],str(file_handler.filename))
      if obj.register_voter(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],result['gender'],result['wardno'],str(file_handler.filename)) ==True:
            return flask.render_template("registration_complete.html",result=result,mapping=mapping,photo="../static/PurpleAdmin-Free-Admin-Template-master/images/"+file_handler.filename,visa=None,candidate=None)
      else:
          return flask.render_template("permission_denied_voter.html")


@app.route("/registration_complete_voter_overseas",methods = ['POST', 'GET'])
def registration_complete_voter_overseas():
    mapping={
        "uid":"Unique ID",
        "fname": "First Name",
        "lname": "Last Name",
        "email": "Email ID",
        "age":"Age",
        "address":"Permanent Address",
        "gender":"Gender",
        "wardno": "Ward No",
        "photo": "Photo Upload",
        "criminal":"Criminal Records",
        "visa": "Visa Upload"
                    }
    if request.method=="POST":
      result=request.form
      file_handler=request.files['photo']
      #file_handler.save(os.path.join("D:\codefundo\Webapp\static\PurpleAdmin-Free-Admin-Template-master\images",secure_filename(file_handler.filename)))
      file_handler.save(os.path.join(data["ImgPath"], secure_filename(result['uid']+".jpg")))
      fh=file_handler
      file_handler=request.files['visa']
      file_handler.save(os.path.join(data["ImgPath"], secure_filename(result['uid']+"_visa.jpg")))
      obj=Voting()

      print(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],str(file_handler.filename))
      if obj.register_voter_overseas(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],result['gender'],result['wardno'],str(fh.filename),str(result['uid']+"_visa.jpg")) ==True:
            return flask.render_template("registration_complete.html",result=result,mapping=mapping,photo="../static/PurpleAdmin-Free-Admin-Template-master/images/"+str(result['uid']+".jpg"),visa="../static/PurpleAdmin-Free-Admin-Template-master/images/"+str(result['uid'])+"_visa.jpg",candidate=None)
    else:
        return flask.render_template("permission_denied_overseas.html")

@app.route("/cast_vote_home")
def cast_vote_home():
  mapping={
    "001":"Bangalore",
    "002":"Delhi",
    "003":"Chennai",
    "004": "Mumbai",
    "005":"Kolkata",
    "006":"Hyderabad"
  }
  global session
  print(session)
  # import pdb; pdb.set_trace()
  cap = cv2.VideoCapture(0)
  obj=Voting()
  import time
  while True:
    time.sleep(3)
    ret, frame = cap.read()
    cv2.imwrite("img.jpg",frame)
    if obj.check_emotion():
      myclient=pymongo.MongoClient(uri)
      mydb = myclient["codefundo"]
      mycol=mydb['cand_reg']
      result=[]
      obj=NewsSearch()
      for x in mycol.find():
        result.append(x)
      news=[]
      # import pdb; pdb.set_trace()
      for res in result:
        news.append(obj.news_candidate(str(res["First Name"]+" "+res['Last Name']+" india election")))
      # import pdb; pdb.set_trace()
      return flask.render_template("cast_vote.html",result=result,news=news,mapping=mapping)
    else:
        return flask.render_template("permission_denied_emotion.html")
    break


# @app.route("/cast_vote")
# def cast_vote():
#   myclient=pymongo.MongoClient(uri)
#   mydb = myclient["codefundo"]
#   mycol=mydb['cand_reg']
#   result=[]
#   for x in mycol.find():
#     result.append(x)
#   # import pdb; pdb.set_trace()
#   return flask.render_template("cast_vote.html",result=result)


@app.route("/voted",methods = ['POST', 'GET'])
def voted():
  if request.method=="POST":
    result=request.form
    # import pdb; pdb.set_trace()
    whom=result['vote']
    import datetime
    import time
    fil=open("vote_tabulate.txt","a+")
    myclient = pymongo.MongoClient(uri)
    mydb = myclient["codefundo"]
    mycol=mydb['cand_reg']
    #########THE LINE THAT FAKES IT#####################
    mycol.update_one({str(whom):"17"},{"$set":{str(whom):"38"}})
    #######################################################
    dic=mycol.find_one({"UID":str(whom)},{str(whom):1,'_id':0})
    candidate_uid=dic[str(whom)]
    dic=mycol.find_one({"UID":str(whom)},{"First Name":1,"Last Name":1,'_id':0})
    # time=datetime.datetime.now()
    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fil.writelines(str(dic["First Name"]+" "+dic['Last Name']+"\t\t"+t))
    # current_votes=mycol.find_one({"UID":whom})['vote_count']
    # mycol.find_one_and_update({"UID":whom},{'$inc':{"vote_count":1}})
    apidata={"workflowFunctionID": 9,"workflowActionParameters": []}
    url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/contracts/"+str(candidate_uid)+"/actions"
    # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
    headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json'
    # import pdb; pdb.set_trace()
    responsefromapi = requests.post(url,json=apidata,headers=headers)
    return flask.render_template("thank_you.html",result=mycol.find_one({"UID":whom}))
  

  # apidata={"workflowFunctionID": 9,"workflowActionParameters": []}
  # url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/contracts/"+str(candidate_uid)+"/actions"
  # # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
  # headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json',
  
  # responsefromapi = requests.post(url,json=apidata,headers=headers)
  # print(responsefromapi.url)
  # print(responsefromapi.status_code)
  # if responsefromapi.status_code == 200:
  #     results=json.loads(responsefromapi.content.decode('utf-8'))
  #     ##TODO DB add this dude has voted
  #     return 'thanks for voting'
  # else:
  #     return 'failed'

  # return 'thanks for voting'

##################################################################################################################
##################################################################################################################
#########################################################
#########################################################
#########################################################
#########################################################


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
      # import pdb; pdb.set_trace()
      if results['capabilities']['canUpgradeWorkbench']==True:
          return ['admin',results['currentUser']['userID']]
      else:
          
          return ['user',results['currentUser']['userID']]
      
  else:
      return 'failed at getting user type'
def getvotecount():
  url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/contracts?workflowId=4"
  # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
  headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json',
  
  responsefromapi = requests.get(url,headers=headers)
  print(responsefromapi.url)
  print(responsefromapi.status_code)
  print(responsefromapi.json())
  if responsefromapi.status_code == 200:
      results=json.loads(responsefromapi.content.decode('utf-8'))
      return results
  else:
      return 'error in getting votes'
@app.route("/getvotes",methods = ['POST', 'GET'])
def getvotes():
  ansstr={}
  votejson= getvotecount()
  for x in votejson['contracts']:
      # f=0
      temp =  'dude number :'+str(x['id'])+':'
      for y in x['contractProperties']:
          if y['workflowPropertyId']==14:
              temp = temp + 'number of votes: '+str(y['value'])+'\n'
              ansstr[str(x['id'])]=y['value']
              # f=1
      # if f==1:
      #     ansstr = ansstr+temp
  return ansstr

      
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
      return render_template('admin_home.html')
@app.route("/launchcandidate",methods = ['POST', 'GET'])
def launchcandidate():
  apidata={
      "workflowFunctionID": 8,
      "workflowActionParameters": [
        {
          "name": "uid",
          "value": "12",
          "workflowFunctionParameterId": 6
        }
      ]
    }
  print(apidata)
  url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/contracts?workflowId=4&contractCodeId=4&connectionId=1"
  # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
  headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json',
  
  responsefromapi = requests.post(url,json=apidata,headers=headers)
  print(responsefromapi.url)
  print(responsefromapi.status_code)
  if responsefromapi.status_code == 200:
      results=json.loads(responsefromapi.content.decode('utf-8'))
      newcontract=results
      print('newcontract')
      print(newcontract)##add to db
      ##TODO add this dude lauched
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

      return 'thanks for registering'
  else:
      return 'failed'

@app.route("/register_msft",methods = ['POST', 'GET'])
def register_msft():
  global session
  data = request.form.to_dict()
  print(data['id_token'])
  # import pdb; pdb.set_trace()
  auth_token=data['id_token']
  session['auth_token']=auth_token
  print(session,"\n\n\n\n\n\n")
  x = getusertype()
  usertype=x[0]
  user_id=x[1]
  fil=str(open("uid.txt","r").read())
  # import pdb; pdb.set_trace()
  myclient = pymongo.MongoClient(uri)
  mydb = myclient["codefundo"]
  mycol=mydb['cand_reg']
  # current_votes=mycol.find_one({"UID":str(fil)})['vote_count']
  mycol.find_one_and_update({"UID":str(fil)},{'$set':{str(fil):user_id}})
  # import pdb; pdb.set_trace()
  if usertype=='user':
      usertype1=getyourroleid()
      if usertype1=='voter':
          return flask.render_template("cast_vote.html")
      else:
          return render_template('home.html')
  else:
      return render_template('admin_home.html')

@app.route("/shobhit_voted",methods = ['POST', 'GET'])
def shobhit_voted():
  global session
  candidate_uid=request.form['uid']
  myclient = pymongo.MongoClient(uri)
  mydb = myclient["codefundo"]
  mycol=mydb['cand_reg']
  # import pdb; pdb.set_trace()
  dic=mycol.find_one({"UID":str(candidate_uid)},{str(candidate_uid):1,'_id':0})
  candidate_uid=dic[str(candidate_uid)]

  apidata={"workflowFunctionID": 9,"workflowActionParameters": []}
  url="https://votemaadi-4bm4ew-api.azurewebsites.net/api/v1/contracts/"+str(candidate_uid)+"/actions"
  # params={'workflowId':1,'contractCodeId':1,'connectionId':1}
  headers={'Authorization': 'Bearer {0}'.format(session['auth_token'])}#{'Content-Type': 'application/json',
  
  responsefromapi = requests.post(url,json=apidata,headers=headers)
  print(responsefromapi.url)
  print(responsefromapi.status_code)
  if responsefromapi.status_code == 200:
      results=json.loads(responsefromapi.content.decode('utf-8'))
      ##TODO DB add this dude has voted
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
  return redirect("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/oauth2/authorize?response_type=id_token%20code&client_id=c80344c2-d7fc-41e1-adcc-dd33683a7f6b&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fregister_msft&state=c0756113-6172-47f2-8afc-666f315c15b1&client-request-id=0de0f9e0-a2f4-4853-9bd2-7326f1f409d1&x-client-SKU=Js&x-client-Ver=1.0.17&nonce=3f993c47-3042-4669-bdce-02024f6c802f&response_mode=form_post")  # return redirect("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/oauth2/v2.0/authorize?client_id=c62087b9-cfed-4105-a9c2-4fd3953ceed5&response_type=id_token&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fshobhit&response_mode=fragment&scope=openid&state=12345&nonce=678910")

@app.route("/redirect_home")
def ext1():    
  # print(data['id_token'])
  return redirect("https://login.microsoftonline.com/kumarshobhit98outlook.onmicrosoft.com/oauth2/authorize?response_type=id_token%20code&client_id=c80344c2-d7fc-41e1-adcc-dd33683a7f6b&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fhome&state=c0756113-6172-47f2-8afc-666f315c15b1&client-request-id=0de0f9e0-a2f4-4853-9bd2-7326f1f409d1&x-client-SKU=Js&x-client-Ver=1.0.17&nonce=3f993c47-3042-4669-bdce-02024f6c802f&response_mode=form_post")


if __name__ == "__main__":
    app.run(debug=True)
