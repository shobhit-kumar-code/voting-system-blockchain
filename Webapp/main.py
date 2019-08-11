import flask
import os
import json
from flask import Flask, render_template, request
import sys
from werkzeug import secure_filename
from vote_system import Voting
import pdb

import cv2
import pymongo
# sys.path.append('D:\EmotionDetection')
# print(sys.path)
# from Mails import Mail

app = flask.Flask(__name__,static_url_path='/static')
fd = open("config.txt")
data = json.load(fd)


@app.route("/")
def home():
     return flask.render_template("home.html")


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
    return flask.render_template("register.html")

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
      if obj.register_candidate(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],result['gender'],result['wardno'],str(file_handler.filename),result['criminal']) ==True:
            return flask.render_template("registration_complete.html",result=result,mapping=mapping,photo="../static/PurpleAdmin-Free-Admin-Template-master/images/"+file_handler.filename,visa=None)

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
            return flask.render_template("registration_complete.html",result=result,mapping=mapping,photo="../static/PurpleAdmin-Free-Admin-Template-master/images/"+file_handler.filename,visa=None)
      else:
          return flask.render_template("permission_denied.html")


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
            return flask.render_template("registration_complete.html",result=result,mapping=mapping,photo="../static/PurpleAdmin-Free-Admin-Template-master/images/"+str(result['uid']+".jpg"),visa="../static/PurpleAdmin-Free-Admin-Template-master/images/"+str(result['uid'])+"_visa.jpg")


@app.route("/cast_vote_home")
def cast_vote_home():
  cap = cv2.VideoCapture(0)
  obj=Voting()
  import time
  while True:
    time.sleep(3)
    ret, frame = cap.read()
    cv2.imwrite("img.jpg",frame)
    if obj.check_emotion():
      myclient=pymongo.MongoClient("mongodb://localhost:27017/")
      mydb = myclient["codefundo"]
      mycol=mydb['cand_reg']
      result=[]
      for x in mycol.find():
        result.append(x)
      # import pdb; pdb.set_trace()
      return flask.render_template("cast_vote.html",result=result)
    else:
        return "Emotional Issue"
    break


@app.route("/cast_vote")
def cast_vote():
  myclient=pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["codefundo"]
  mycol=mydb['cand_reg']
  result=[]
  for x in mycol.find():
    result.append(x)
  # import pdb; pdb.set_trace()
  return flask.render_template("cast_vote.html",result=result)


@app.route("/voted",methods = ['POST', 'GET'])
def voted():
  if request.method=="POST":
    result=request.form
    whom=result['vote']
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["codefundo"]
    mycol=mydb['cand_reg']
    current_votes=mycol.find_one({"UID":whom})['vote_count']
    mycol.find_one_and_update({"UID":whom},{'$inc':{"vote_count":1}})
    # import pdb; pdb.set_trace()
    return flask.render_template("thank_you.html",result=mycol.find_one({"UID":whom}))


if __name__ == "__main__":
    app.run(debug=True)
