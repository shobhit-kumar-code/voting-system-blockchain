import flask
import os
import json
from flask import Flask, render_template, request
import sys
from werkzeug import secure_filename
from vote_system import Voting
import pdb
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

@app.route("/registration_complete_candidate",methods = ['POST', 'GET'])
def registration_complete_candidate():
    mapping={
            "uid":"Unique ID",
            "fname": "First Name",
            "lname": "Last Name",
            "email": "Email ID",
            "age":"Age",
            "address":"Permanent Address",
            "photo": "Photo Upload",
            "criminal":"Criminal Records"
                      }
    if request.method=="POST":
      result=request.form
      file_handler=request.files['photo']
      #file_handler.save(os.path.join("D:\codefundo\Webapp\static\PurpleAdmin-Free-Admin-Template-master\images",secure_filename(file_handler.filename)))
      file_handler.save(os.path.join(data["ImgPath"],secure_filename(file_handler.filename)))
      obj=Voting()
      if obj.register_candidate(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],str(file_handler.filename),result['criminal']) ==True:
            return flask.render_template("registration_complete.html",result=result,mapping=mapping,photo="../static/PurpleAdmin-Free-Admin-Template-master/images/"+file_handler.filename)

@app.route("/registration_complete_voter",methods = ['POST', 'GET'])
def registration_complete_voter():
    mapping={
        "uid":"Unique ID",
        "fname": "First Name",
        "lname": "Last Name",
        "email": "Email ID",
        "age":"Age",
        "address":"Permanent Address",
        "photo": "Photo Upload",
        "criminal":"Criminal Records"
                    }
    if request.method=="POST":
      result=request.form
      file_handler=request.files['photo']
      #file_handler.save(os.path.join("D:\codefundo\Webapp\static\PurpleAdmin-Free-Admin-Template-master\images",secure_filename(file_handler.filename)))
      file_handler.save(os.path.join(data["ImgPath"], secure_filename(file_handler.filename)))

      obj=Voting()

      print(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],str(file_handler.filename))
      if obj.register_voter(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],str(file_handler.filename)) ==True:
            return flask.render_template("registration_complete.html",result=result,mapping=mapping,photo="../static/PurpleAdmin-Free-Admin-Template-master/images/"+file_handler.filename)
if __name__ == "__main__":

    app.run(debug=True)
