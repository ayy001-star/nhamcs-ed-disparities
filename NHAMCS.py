import pandas as pd

df = pd.read_stata("ed2022-stata.dta", convert_categoricals=False)
df[["WAITTIME", "RACERETH", "IMMEDR", "AGE", "SEX"]].describe()