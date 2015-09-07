import os

from flask import Flask, render_template, request, redirect, session, url_for, flash
import json
import logging

import config
import setupdata



app = Flask(__name__)
app.config.from_object(config)

logging.basicConfig(filename="/var/log/Bot/bot.log", level=logging.DEBUG)

@app.route("/")
def index():
    return redirect(url_for("about"))

@app.route("/classifiers")
def classifiers():
    return render_template("classifiers.html")

@app.route("/classifiers/compare", methods=["POST"])
def compare():
    message = request.form.get("message")
    details = setupdata.comparison(message)
    features = details["features"]
    bayesclassification = details["Thomas"]
    fisherclassification = details["Ronald"]
    return render_template("retrieved.html", message=message, features=features, 
                            bayesclassification=bayesclassification, fisherclassification=fisherclassification)

@app.route("/classifiers/stats", methods=["POST"])
def stats():
    retrieved = request.form.get("stats")
    details = setupdata.stats(retrieved)
    print details
    message = details["message"]
    features = details["features"]
    negprobability = details["docprob"]["negative"]
    posprobability = details["docprob"]["positive"]
    classification = details["classification"]
    return render_template("stats.html", message=message, features=features, 
        negprobability=negprobability, posprobability=posprobability, 
        classification=classification)

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/maker")
def maker():
    return render_template("maker.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/500.html")
def fivehundred():
    return render_template("500.html")

if __name__ == "__main__":
    app.run(debug = True)
