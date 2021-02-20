from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')
@app.route('/index')
def index():
    return render_template('index.html')