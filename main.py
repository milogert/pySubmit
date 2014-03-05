import flask #from flask import Flask, render_template

myApp = flask.Flask(__name__)

@myApp.route('/')
def index():
  if flask.session["present"]:
    return flask.redirect(flask.url_for(str(flask.session["role"])))

  return flask.render_template("index.html")

@myApp.route("/login", methods=["GET", "POST"])
def login():
  if flask.request.method == "POST":
    flask.session["present"] = True
    flask.session["username"] = flask.request.form["username"]
    flask.session["role"] = flask.request.form["role"]
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

@myApp.errorhandler(404)
def notFound(theError):
  return theError

myApp.secret_key="\xd0\x9f\xab\xa1\xd5k\xbaa\xc7\x8d!\x027\xa2X\x8fS}4~\xb2\xcb\x89l"

if __name__ == '__main__':
  myApp.run(
    debug=True,
    host="0.0.0.0"
  )