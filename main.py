from flask import Flask, render_template, url_for, request, redirect
from Names import find_name, compare_names, general_statistics
from tempfile import NamedTemporaryFile
import os, glob

app = Flask(__name__)
@app.route('/')
def index():
    png_files = glob.glob('static/*.png')
    for png_file in png_files:
        os.remove(png_file)
    return render_template('index.html')

@app.route('/statistic/', methods=['POST', 'GET'])
def statistic():
    import matplotlib
    matplotlib.use('Agg')
    name = str(request.form.get('name'))
    year_beginning = str(request.form.get('beginning'))
    year_end = str(request.form.get('end'))

    diagram = find_name(name, year_beginning, year_end)

    return render_template('statistic.html', diagram=diagram)


@app.route('/compare/', methods=['POST', 'GET'])
def compare():
    return render_template('compare.html')

@app.route('/general-statistics/', methods=['POST', 'GET'])
def general_statistics():
    return render_template('general-statistics.html')

if __name__ == '__main__':
    app.run(debug=True)