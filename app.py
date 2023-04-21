from flask import Flask,render_template,url_for,request,jsonify
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import datetime
import pickle

app = Flask(__name__,template_folder="templates")
model = pickle.load(open("./models/filename.pkl","rb")) 
print("Model Loaded")

@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")

@app.route("/predict",methods=['GET','POST'])
@cross_origin()
def predict():
   if request.method == 'POST':
        date = request.form['date']
        day = int(pd.to_datetime(date,format="%Y-%m-%d").day)
        month = int(pd.to_datetime(date,format="%Y-%m-%d").month)
        #minTemp
        mintempC=float(request.form['mintemp'])
        #maxTemp
        maxtempC=float(request.form['maxtemp'])
        #humidity
        humidity=float(request.form['humidity'])
        #dewPoint
        DewPointC = float(request.form['dewpoint'])
        #pressure
        pressure = float(request.form['pressure'])
        #cloudcover
        cloudcover = float(request.form['cloudcover'])
        #visibility
        visibility = float(request.form['visibility'])
        #Rainfal
        precipMM = float(request.form['precipMM'])
        #RainToday
        RainToday = int(request.form['raintoday'])
        
        input_lst = [maxtempC,mintempC,DewPointC,cloudcover,humidity,pressure,visibility,precipMM,RainToday,day,month]
        pred = model.predict([input_lst])
        output = pred
        if output == 0:
           return render_template("after_sunny.html")
        else: 
           return render_template("after_rainy.html")
	
   return render_template("predict.html")

if __name__== "__main__":
    app.run(port=8000,debug=True)