import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
from tempfile import NamedTemporaryFile

df = pd.read_csv('source/nat1900-2017.tsv', sep='\t')
df.rename(columns={"sexe":"Gender", "preusuel":"Name","annais":"Years","nombre":"Number of newborns"}, inplace=True)
df.Years = pd.to_numeric(df.Years,errors='coerce')

def find_name(name, year_beginning, year_end):
    my_filter = lambda name: df.Name == name
    results = df[my_filter(name.upper())]

    filter_years = (df.Years >= int(year_beginning)) & (df.Years <= int(year_end))
    results = results[filter_years]
    results.set_index('Years', inplace=True)
   
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

    return diagram_png

def compare_names(name1, name2):
    pass

def general_statistics():
    pass
