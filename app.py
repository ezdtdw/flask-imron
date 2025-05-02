from flask import Flask, render_template, request, redirect, url_for 
from PIL import Image, ImageEnhance, ImageFilter 
import cv2 
import os 
import numpy as np 
 
app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = 'static/uploads/' 
 
@app.route('/') 
def index(): 
    return render_template('index.html') 
 
@app.route('/upload', methods=['POST']) 
def upload(): 
    if 'file' not in request.files: 
        return redirect(url_for('index')) 
 
    file = request.files['file'] 
    if file.filename == '': 
        return redirect(url_for('index')) 
 
    if file: 
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) 
        file.save(filepath) 
 
        img = Image.open(filepath) 
 
        img = improve_image_quality(img) 
 
        processed_filename = 'processed_' + file.filename 
        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 
processed_filename) 
        img.save(processed_filepath) 
 
        return render_template('index.html', original_filename=file.filename, 
processed_filename=processed_filename) 
 
def improve_image_quality(img): 
    img = img.convert('L') 
 
    enhancer = ImageEnhance.Contrast(img) 
    img = enhancer.enhance(1.5) 
 
    img = cv2.cvtColor(np.array(img), cv2.COLOR_GRAY2BGR)  
    img = cv2.GaussianBlur(img, (5, 5), 0) 
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)) 
  
    img = img.filter(ImageFilter.SHARPEN) 
 
    return img 
 
if __name__ == '__main__': 
    app.run(debug=True) 