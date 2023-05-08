import pandas as pd

df = pd.read_csv("relatorio_algebra linear.csv")
df = df.drop(0)
print(df)
