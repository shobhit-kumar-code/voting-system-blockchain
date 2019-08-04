import flask
import os
import json
from flask import Flask, render_template, request
import sys
from vote_system import Voting
# sys.path.append('D:\EmotionDetection')
# print(sys.path)
# from Mails import Mail

app = flask.Flask(__name__,static_url_path='/static')

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
    if request.method=="POST":
      result=request.form
      print(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],result['photo'],result['criminal'])
      obj=Voting()
      if obj.register_candidate(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],result['photo'],result['criminal']) ==True:
            return flask.render_template("registration_complete.html",result=result)

@app.route("/registration_complete_voter",methods = ['POST', 'GET'])
def registration_complete_voter():
    if request.method=="POST":
      result=request.form
      obj=Voting()
      if obj.register_voter(result['uid'],result['fname'],result['lname'],result['age'],
          result['address'],result['photo']) ==True:
            return flask.render_template("registration_complete.html",result=result)
if __name__ == "__main__":

    app.run(debug=True)
