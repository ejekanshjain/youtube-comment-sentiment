
from flask import Flask, request,jsonify, render_template
import pandas as pd
import json
import plotly
import plotly.graph_objs as go
import analyzer

import sys



server = Flask(__name__, template_folder='templates')


@server.route("/")
def hello():

   return render_template("cards.html")


@server.route("/cards", methods=["GET","POST"])
def predict():
    video = request.form['search']
    region = request.form['country']
    category = request.form['Category']
    try:
        total,channel_title,video_id = (analyzer.data(region,category,video))
        total = dict(total)
        print(total)
        # print(type(total))
        render = "https://www.youtube.com/embed/"+video_id
        print(render)
        return render_template("dash.html", Positive=round(total['pos'],2),Negative=round(total['neg'],2),Neutral=round(total['neu'],2),channel = channel_title,videoID=render)
    except Exception as e:
        return render_template("error_404.html", error=str(e))


@server.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html'), 404


if __name__ == '__main__':
    # try:
    #     port = int(sys.argv[1]) # This is for a command-line input
    # except:
    #     port = 12345 # If you don't provide any port the port will be set to 12345

    # lr = joblib.load("model.pkl") # Load "model.pkl"
    # print ('Model loaded')
    # model_columns = joblib.load("model_columns.pkl") # Load "model_columns.pkl"
    # print ('Model columns loaded')
    # port=port,
    server.run(debug=True)
