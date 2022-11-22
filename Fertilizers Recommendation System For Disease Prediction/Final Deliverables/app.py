import requests
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from tensorflow.python.keras.backend import set_session
import openpyxl

#initialize flask app
app  = Flask(__name__)

# load models
veg_model = load_model("vegetable.h5")
fruit_model = load_model("fruit.h5")

#home page
@app.route('/')
def home():
    return render_template("home.html")

#prediction page
@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        f = request. files["image"]
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename (f.filename))
        f. save(file_path)
        img = image.load_img(file_path, target_size=(128, 128))
        X = image.img_to_array(img)
        X = np.expand_dims(X, axis=0)
        plant=request.form['PLANT TYPE']
        print (plant)
        if (plant=="vegetable"):
            preds = veg_model. predict(X)
            df=pd.read_excel('precautions-veg.xlsx')
            output = df. iloc [preds [0]]['caution'][0]
        else:
            preds = fruit_model.predict(X)
            df=pd.read_excel('precautions - fruits.xlsx')
            output = df. iloc [preds [0]]['caution']
        return output
    return render_template('output.html',result=output)

if __name__ == "__main__":
    app.run(debug = True, port = 8080)
