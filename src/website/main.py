import base64
from flask import Flask, render_template, request
import cv2
import numpy as np
from ml import bananalyze

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/camera', methods=['GET', 'POST'])
def camera():
    if request.method == 'POST':
        # Decode image into a form that we can use
        content = request.form['file'].split(';')[1]
        image_encoded = content.split(',')[1]
        body = base64.decodebytes(image_encoded.encode('utf-8'))
        im_arr = np.frombuffer(body, dtype=np.uint8)
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        # Run banalysis
        score = bananalyze(img)

        return str(score)
    else:
        return render_template('camera.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
