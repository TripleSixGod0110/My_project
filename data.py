import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/ThuwarakeshM/geting-started-with-plottly-dash/main/life_expectancy.csv',
                sep=',')
all_cont = df['continent'].unique()
