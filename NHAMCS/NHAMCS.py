import pandas as pd

df = pd.read_stata("ed2022-stata.dta", convert_categoricals=False)
print(df[["WAITTIME", "RACERETH", "IMMEDR", "AGE", "SEX"]].describe())

print(df['ARRTIME'].dtype)
df['ARRTIME'].value_counts(dropna=False).head(20)