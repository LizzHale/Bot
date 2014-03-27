import os

from flask import Flask, render_template, request, redirect, session, url_for, flash

import config


app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    return redirect(url_for("welcome"))

@app.route("/welcome")
def welcome():
    name = "Lizz"
    return render_template("kiwi.html", name = name)

if __name__ == "__main__":
    app.run(debug = True)
