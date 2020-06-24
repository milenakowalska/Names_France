from flask import Flask, render_template, url_for, request, redirect
from Names import find_name
from tempfile import NamedTemporaryFile
import os

os.chdir(os.path.dirname(__file__))
app = Flask(__name__)
# app._static_folder = os.path.dirname(__file__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/statistic/', methods=['POST', 'GET'])
def statistic():
    import matplotlib
    matplotlib.use('Agg')
    name = request.form.get('name')
    diagram = find_name(str(name))

    return render_template('statistic.html', diagram=diagram)


if __name__ == '__main__':
    app.run(debug=True)