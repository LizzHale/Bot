import os

from flask import Flask, render_template, request, redirect, session, url_for, flash

import config
import setupdata


app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    return redirect(url_for("classifiers"))

@app.route("/classifiers")
def classifiers():
    details = setupdata.comparison("Instead this cringe-making novel takes the sappy contrivances of his 2001 book, 'How to be Good,' to an embarrassing new low.")
    message = details["message"]
    features = details["features"]
    bayesclassification = details["Thomas"]
    fisherclassification = details["Ronald"]
    return render_template("classifiers.html", message=message, features=features, 
                            bayesclassification=bayesclassification, fisherclassification=fisherclassification)

@app.route("/chat")
def chat():
    details = setupdata.stats("Despite the rave reviews, the restaurant was terrible")
    message = details["message"]
    features = details["features"]
    negprobability = details["docprob"]["negative"]
    posprobability = details["docprob"]["positive"]
    classification = details["classification"]
    return render_template("chat.html", message=message, features=features, 
        negprobability=negprobability, posprobability=posprobability, 
        classification=classification)

@app.route("/maker")
def maker():
    return render_template("maker.html")


if __name__ == "__main__":
    app.run(debug = True)
