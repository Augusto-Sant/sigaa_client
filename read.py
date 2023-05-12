import pandas as pd
import os

dataframes = []
for file_name in os.listdir("./relatorios"):
    if file_name.endswith(".csv"):
        df = pd.read_csv(f"relatorios/{file_name}")
        df = df.drop(0)
        df = (
            df.drop("Matrícula", axis=1).drop("Nome", axis=1).drop("Unnamed: 0", axis=1)
        )

        titulo = (
            file_name.replace("relatorio_", "")
            .replace(".csv", "")
            .replace("_", " ")
            .upper()
        )

        # add the (somename) as a new column to the dataframe
        df["Titulo"] = titulo

        print(df)
        dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)
print("MERGED:")
print(merged_df)
