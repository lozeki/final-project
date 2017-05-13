from flask import Flask, render_template

import prometheus_metrics

app = Flask(__name__)

from prometheus_metrics import setup_metrics
setup_metrics(app)

@app.route('/')
def home():

    return render_template('main.html')

@app.route('/practice')
def practice():

    return render_template('practice.html')

@app.route('/poses')
def poses():

    return render_template('poses.html')

@app.route('/about')
def about():

    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
