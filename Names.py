import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os

df = pd.read_csv(os.path.join(os.path.dirname(__file__),'nat1900-2017.tsv'), sep='\t', index_col='annais')
df = df.drop('XXXX')
df.index = pd.to_numeric(df.index,errors='coerce')

my_filter = lambda name: df['preusuel'] == name

def find_name(name):
    results = df[my_filter(name.upper())]
    popularity = results['nombre']
    list_of_values = []
    for key, value in popularity.items():
        for x in range(value):
            list_of_values.append(key)
    my_bins = [1900,1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2020]
    plt.hist(list_of_values,bins=my_bins, edgecolor='#595959', color='#ff7b64')
    plt.xticks(np.arange(1900,2030,10),labels=my_bins)
    plt.gcf().autofmt_xdate(rotation = 30)
    plt.xlabel('Years')
    plt.title(f'Popularity of the name "{name}" in France')
    plt.show()

find_name('Robert')