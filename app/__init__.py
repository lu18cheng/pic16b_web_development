# to run this website and watch for changes: 
# $ export FLASK_ENV=development; flask run


from flask import Flask, g, render_template, request

import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pickle

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import base64


# Create web app, run with flask run
# (set "FLASK_ENV" variable to "development" first!!!)

app = Flask(__name__)

# Create main page (fancy)

@app.route('/')

# def main():
#     return render_template("main.html")

# comment out the below to focus on just the fundamentals

# after running
# $ export FLASK_ENV=development; flask run
# site will be available at 
# http://localhost:5000

def main():
    return render_template('main_better.html')
    # return render_template('main.html')

# Show url matching

@app.route('/hello/')
def hello():
    return render_template('hello.html')

@app.route('/hello/<name>/')
def hello_name(name):
    return render_template('hello.html', name=name)

# Page with form

@app.route('/ask/', methods=['POST', 'GET'])
def ask():
    if request.method == 'GET':
        return render_template('ask.html')
    else:
        try:
            return render_template('ask.html', name=request.form['name'], student=request.form['student'])
        except:
            return render_template('ask.html')

# File uploads and interfacing with complex Python
# basic version

@app.route('/submit-basic/', methods=['POST', 'GET'])
def submit_basic():
    if request.method == 'GET':
        return render_template('submit-basic.html')
    else:
        try:
            return render_template('submit-basic.html', thanks = True)
        except:
            return render_template('submit-basic.html', error=True)

# nontrivial version: makes a prediction and shows a viz
@app.route('/submit-advanced/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            # retrieve the image
            img = request.files['image']
            img = np.loadtxt(img)
            
            # reshape into appropriate format for prediction
            x = img.reshape(1, 64)
            
            # load up a pre-trained model and get a prediction
            model = pickle.load(open("mnist-model/model.pkl", 'rb'))
            d = model.predict(x)[0]

            # plot the image itself
            fig = Figure(figsize = (3, 3))
            ax = fig.add_subplot(1, 1, 1,)
            ax.imshow(img, cmap = "binary")
            ax.axis("off")
            
            # in order to show the plot on flask, we need to do a few tricks
            # Convert plot to PNG image
            # need to: 
            # import io 
            # import base64 
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)
            
            # Encode PNG image to base64 string
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            
            # finally we can render the template with the prediction and image
            return render_template('submit.html', digit=d, image=pngImageB64String)
        except:
            return render_template('submit.html', error=True)