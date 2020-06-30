from flask import Flask, render_template, url_for, request, redirect
from Names import find_name, compare_names, general_statistics
from tempfile import NamedTemporaryFile
import os, glob, time
import pandas as pd

app = Flask(__name__)
@app.route('/')
def index():
    png_files = glob.glob('static/*.png')
    for png_file in png_files:
        minutes_30 = time.time() - 30 * 60
        if os.path.getatime(png_file) < minutes_30:
                os.remove(png_file)
    return render_template('index.html')

@app.route('/statistic/', methods=['POST', 'GET'])
def statistic():
    import matplotlib
    matplotlib.use('Agg')
    name = str(request.form.get('name'))
    year_beginning = str(request.form.get('beginning'))
    year_end = str(request.form.get('end'))

    diagram, DataFrame = find_name(name, year_beginning, year_end)

    return render_template('statistic.html', diagram=diagram, DataFrame = DataFrame.to_html())


@app.route('/compare/', methods=['POST', 'GET'])
def compare():
    import matplotlib
    matplotlib.use('Agg')
    name1 = str(request.form.get('name_first'))
    name2 = str(request.form.get('name_second'))

    compare_names_diagram, compare_DataFrame = compare_names(name1, name2)

    return render_template('compare.html', compare_names_diagram=compare_names_diagram, compare_DataFrame = compare_DataFrame.to_html(), n1 = name1, n2=name2)

@app.route('/general-statistics/', methods=['POST', 'GET'])
def general_statistics():
    most_popular_df=pd.read_csv('static/most_popular_.csv')
    most_popular_df.index += 1

    df_female=pd.read_csv('static/most_popular_female.csv')
    df_female.index +=1
    df_male=pd.read_csv('static/most_popular_male.csv')
    df_male.index += 1
    return render_template('general-statistics.html', 
                            most_popular_df=most_popular_df.to_html(),
                            df_female = df_female.to_html(),
                            df_male = df_male.to_html(),
                                )

if __name__ == '__main__':
    app.run(debug=True)