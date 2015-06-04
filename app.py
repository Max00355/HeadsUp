import flask
from pymongo import MongoClient
import random
import string

app = flask.Flask(__name__)
db = MongoClient("localhost", 27017).headsup

@app.route("/", methods=['GET', 'POST'])
def add():
    if flask.request.method == "POST":
        words = flask.request.form['words'].split(",")
        time = len(words) * int(flask.request.form['time']) # Seconds are in seconds per card, so say there are 10 cards and the person gives 5 seconds per card it should take 50 seconds for the set.
        generate = ''.join([random.choice(string.uppercase+string.lowercase+string.digits) for x in range(5)])
        while db.games.find_one({"id":generate}):
            generate = ''.join([random.choice(string.uppercase+string.lowercase+string.digits) for x in range(5)])
        db.games.insert({"id":generate, "seconds":time, "words":words})
        return flask.redirect("/{}".format(generate))

    return flask.render_template("add.html")

@app.route("/<_id>")
def play(_id):
    check = db.games.find_one({"id":_id})
    if not check:
        return flask.redirect("/")
    
    words = check['words']
    seconds = check['seconds']
    return flask.render_template("play.html", seconds=seconds, words = str(words).replace("u'", "'"))


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
