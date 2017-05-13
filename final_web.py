from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('main.html')

@app.route('/practice')
def practice():

    return render_template('practice.html')

@app.route('/poses')
def poses():

    return render_template('poses.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
