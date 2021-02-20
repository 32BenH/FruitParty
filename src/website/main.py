from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')
@app.route('/About')
def about():
    return render_template('about.html')
@app.route('/Camera')
def camera():
    return render_template('camera.html')
