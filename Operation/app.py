from flask import Flask, render_template, request, redirect, session, url_for, flash


app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    return redirect(url_for("welcome"))

@app.route("/welcome")
def welcome():
    name = "Lizz"
    return render_template("kiwi.html", name = name)

if __name__ == "__main__":
    app.run(debug = True)