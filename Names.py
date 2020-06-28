import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
from tempfile import NamedTemporaryFile

dataframe = pd.read_csv('source/nat1900-2017.tsv', sep='\t')
dataframe.rename(columns={"sexe":"Gender", "preusuel":"Name","annais":"Years","nombre":"Number of newborns"}, inplace=True)
dataframe.set_index('Years', inplace=True)
dataframe = dataframe.drop('XXXX')
dataframe.index = pd.to_numeric(dataframe.index,errors='coerce')

def find_name(name, year_beginning, year_end):
    my_filter = lambda name: dataframe.Name == name
    results = dataframe[my_filter(name.upper())]

    filter_years = (dataframe.index >= int(year_beginning)) & (dataframe.index <= int(year_end))
    results = results[filter_years]
   
    popularity = results['Number of newborns']
    list_of_values = []
    for key, value in popularity.items():
        for x in range(value):
            list_of_values.append(key)
    my_bins = [x for x in range(int(year_beginning), int(year_end)+10, 10)]
    plt.hist(list_of_values,bins=my_bins, edgecolor='#595959', color='#ff7b64')
    plt.xticks(np.arange(int(year_beginning), int(year_end)+10, 10),labels=my_bins)
    plt.gcf().autofmt_xdate(rotation = 30)
    plt.xlabel('Years')
    plt.title(f'Popularity of the name "{name}" in France')

    diagram = NamedTemporaryFile(
        dir = os.path.join(os.path.dirname(__file__),'static'),
        suffix = '.png', delete=False)

    plt.savefig(diagram)
    diagram_png = os.path.basename(diagram.name)
    diagram.close()

    # customize DataFRame
    results.Gender = results.Gender.map({1:'male', 2:'female'})
    results = results.loc[:, ['Gender','Number of newborns']]

    results = results.groupby(pd.cut(results.index, np.arange(int(year_beginning), int(year_end)+10, 10))).sum()

    indexes = [''.join((str(x), '-', str(x+10))) for x in range(int(year_beginning), int(year_end), 10)]
    results.index = indexes

    return diagram_png, results

def compare_names(name1, name2):
    my_filter = lambda name: dataframe.Name == name

    name_first = dataframe[my_filter(name1.upper())]
    name_second = dataframe[my_filter(name2.upper())]

    values_first_name = []
    values_second_name = []

    results_first = name_first['Number of newborns']
    results_second = name_second['Number of newborns']

    for key, value in results_first.items():
        for x in range(value):
            values_first_name.append(key)

    for key, value in results_second.items():
        for x in range(value):
            values_second_name.append(key)

    my_bins = [x for x in range(1900, 2030, 10)]
    width = 10
    plt.hist(values_first_name,bins=my_bins, alpha=0.5, width=width, edgecolor='#595959', color='#ff7b64', label=f'{name1}', log=True)
    plt.hist(values_second_name,bins=my_bins, alpha=0.5, width=width, edgecolor='#595959', color='#6985a0', label=f'{name2}', log=True)
    plt.xticks(np.arange(1900, 2030, 10),labels=my_bins)
    plt.gcf().autofmt_xdate(rotation = 30)
    plt.xlabel('Years')
    plt.title(f'Comparision of the names: "{name1}" and "{name2}" in France')
    plt.legend([f'{name1}', f'{name2}'])

    diagram = NamedTemporaryFile(
        dir = os.path.join(os.path.dirname(__file__),'static'),
        suffix = '.png', delete=False)

    plt.savefig(diagram)
    diagram_png = os.path.basename(diagram.name)
    diagram.close()
    plt.clf()


    # # customize DataFRame

    result_first = name_first['Number of newborns'].groupby(pd.cut(name_first.index, np.arange(1900,2030, 10))).sum()
    indexes = [''.join((str(x), '-', str(x+10))) for x in range(1900,2020, 10)]
    result_first.index = indexes
    result_first = pd.concat([result_first, pd.Series([f'{name1}' for x in range(12)], index=indexes, name='Name')], axis=1)
    
    result_second = name_second['Number of newborns'].groupby(pd.cut(name_second.index, np.arange(1900,2030, 10))).sum()
    indexes = [''.join((str(x), '-', str(x+10))) for x in range(1900,2020, 10)]
    result_second.index = indexes
    result_second = pd.concat([result_second, pd.Series([f'{name2}' for x in range(12)], index=indexes, name='Name')], axis=1)
    
    results = pd.concat([result_first, result_second], axis=1)

    return diagram_png, results

def general_statistics():
    pass
