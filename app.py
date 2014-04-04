import os

from flask import Flask, render_template, request, redirect, session, url_for, flash
import json

import config
import setupdata



app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    return redirect(url_for("classifiers"))

@app.route("/classifiers")
def classifiers():
    return render_template("classifiers.html")

@app.route("/classifiers", methods=["POST"])
def compare():
    message = request.form.get("message")
    details = setupdata.comparison(message)
    print message
    features = details["features"]
    bayesclassification = details["Thomas"]
    fisherclassification = details["Ronald"]
    return render_template("retrieved.html", message=message, features=features, 
                            bayesclassification=bayesclassification, fisherclassification=fisherclassification)

@app.route("/chat" method=["POST"])
def stats():
    details = setupdata.stats("Despite the rave reviews, the restaurant was terrible")
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


if __name__ == "__main__":
    app.run(debug = True)
