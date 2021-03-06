from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm    
import pandas as pd
import csv
from werkzeug import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        
        
def read_csv():
    for layer in layers:
        df=pd.read_csv('csv')
        lst+'layer' = df['layer'].abs()
        

@app.route("/")
def index():
        
    df=pd.read_csv('300_5000.csv')
    lst1 = df['7'].abs()
    
    df=pd.read_csv('300_5000.csv')
    lst2 = df['8']
    
    df=pd.read_csv('300_5000.csv')
    lst3 = df['9']
    
    fig = plt.figure
    fig,ax = plt.subplots()
    ax.set_xlim(lst2.min(), lst2.max()+0.8) 
    
    ims = []
        
    for i ,n,g in zip(lst3,lst1, lst2):
        x1 = 3
        y1 = i
        x2 = 1
        y2 = n
        x3 = 2
        y3 = g
        
        im3 = plt.barh(x3, y3,color = cm.plasma(g/lst1.max()))
        im2 = plt.barh(x2, y2,color = cm.plasma(n/lst1.max()))
        im = plt.barh(x1, y1,color = cm.plasma(i/lst1.max()))
        
        
        ims.append(im3+im2+im)
        plt.title("D")
        
 
    anim = animation.ArtistAnimation(fig,ims)
    
    FPS = 30

    anim.save('static/img/anim' + str(FPS) + '.gif',
              writer="imagemagick",
              fps = FPS
              )
    
    return render_template(
            "index.html", 
            image = 'static/img/anim' + str(FPS) + '.gif'
            )
@app.route("/form")
def show_csv():
    if request.method == 'POST':
        send_data = request.files['send_data']
        if send_data and allowed_file(send_data.filename):
            filename = secure_filename(send_data.filename)
            send_data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            f = open('uploads/' + filename, 'r')
            f_reader = csv.reader(f)
            result = list(f_reader)

            return render_template('csv.html', result=result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)