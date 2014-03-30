import os

from flask import Flask, render_template, request, redirect, session, url_for, flash

import config


app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    return redirect(url_for("classifiers"))

@app.route("/classifiers")
def classifiers():
    # Mock up is based on the fisher classifier
    message = "Despite the rave reviews, the restaurant was terrible"
    features = {'rave': 1, 'reviews': 1, 'restaurant': 1, 'terrible': 1, 'despite': 1}
    probability_of_positive = 0.659065812937*100
    probability_of_negative = 0.68747796392*100
    classification = "negative"
    return render_template("classifiers.html", message=message, features=features, 
                            probability_of_negative=probability_of_negative, 
                            probability_of_positive=probability_of_positive,
                            classification=classification)

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.rout("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug = True)
