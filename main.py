#!/usr/bin/exec python2

# Import modules.
import flask #from flask import Flask, render_template
import hashlib
import sqlite3

# Import user modules.
import model

# Create the application.
myApp = flask.Flask(__name__)

## Home pages. ###############################################################
@myApp.route('/')
def index():
  if flask.session.has_key("present") and flask.session["present"]:
    return flask.redirect(flask.url_for(str(flask.session["role"])))

  return flask.render_template("index.html")
##############################################################################

## User pages. ###############################################################
@myApp.route("/admin", methods=["GET", "POST"])
def admin():
  """Default admin login is:
    Username: su
    Password: musicalpurplesnakeafternoon
  """
  # if flask.request.method == "POST":
    # aResp = flask.request.form[""]
    # model.addUsers
  if not flask.session["present"]:
    return flask.redirect(flask.url_for("login"))

  if flask.session.has_key("role") and flask.session["role"] == "admin":
    return flask.render_template("admin.html", theUsers=model.getUsers())

  return flask.redirect(flask.url_for("forbidden"))

@myApp.route("/contestant")
def contestant():
  if not flask.session["present"]:
    return flask.redirect(flask.url_for("login"))

  if flask.session.has_key("role") and flask.session["role"] == "contestant":
    return flask.render_template("contestant.html")

  return flask.redirect(flask.url_for("forbidden"))

@myApp.route("/judge")
def judge():
  if not flask.session["present"]:
    return flask.redirect(flask.url_for("login"))

  if flask.session.has_key("role") and flask.session["role"] == "judge":
    return flask.render_template("judge.html")

  return flask.redirect(flask.url_for("forbidden"))
##############################################################################

## Session pages. ############################################################
@myApp.route("/login", methods=["GET", "POST"])
def login():
  if flask.request.method == "POST":
    # Open a connection to the database.
    aConn = sqlite3.connect("pySubmit.db")
    aCursor = aConn.cursor()

    # Query for the username.
    aUname = (str(flask.request.form["username"]),)
    aCursor.execute("SELECT * FROM users WHERE username=? LIMIT 1", aUname)
    aResult = aCursor.fetchone()

    # Close the connection.
    aConn.close()

    # Check password.
    aHash = hashlib.sha224(str(flask.request.form["password"])).hexdigest()
    if aResult and aResult[1] == aHash:
      flask.session["present"] = True
      flask.session["username"] = aResult[0]
      flask.session["role"] = aResult[2]
      return flask.redirect(flask.url_for("index"))

  if flask.session["present"]:
    return flask.redirect(flask.url_for(str(flask.session["role"])))

  return flask.render_template("login.html")

@myApp.route("/logout")
def logout():
  flask.session["present"] = False
  flask.session.pop("username", None)
  flask.session.pop("role", None)

  return flask.redirect(flask.url_for("index"))

@myApp.route("/session")
def session():
  aRet = "Session:\t{0}<br />Username:\t{1}<br />Role:\t\t{2}"
  return aRet.format(
    flask.session["present"],
    flask.session["username"],
    flask.session["role"]
  )
##############################################################################

## Error pages. ##############################################################
@myApp.errorhandler(404)
def notFound(theError):
  return flask.render_template("blank.html", stuff=theError)

@myApp.route("/forbidden")
def forbidden():
  aHtml = """
    <p>
      Looks like you weren't supposed to be going to the page you tried to go to!
    </p>

    <p>
      We won't report you, but try heading back to your <a href='/{0}'>main page</a>. That would be for the best.
    </p>
  """

  return flask.render_template("blank.html", theStuff=aHtml.format(str(flask.session["role"])))
##############################################################################

myApp.secret_key="\xd0\x9f\xab\xa1\xd5k\xbaa\xc7\x8d!\x027\xa2X\x8fS}4~\xb2\xcb\x89l"

if __name__ == '__main__':
  myApp.run(
    debug=True,
    host="0.0.0.0"
  )