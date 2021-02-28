import pandas as pd

df = pd.read_csv('tmp/all.csv')

df.to_excel('tmp/all.xlsx')