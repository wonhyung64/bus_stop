#%%
import os
import sys
import numpy as np
import pandas as pd

# %%
def preprocess_scheme1(df):
    df = df.drop("등록일자", axis="columns")
    df["버스정류장ARS번호"] = df["버스정류장ARS번호"].replace("~", 0).astype("int64")
    df["버스정류장ARS번호_Text"] = df["버스정류장ARS번호"].astype("string").str.pad(width=5, side="left", fillchar="0")
    col_order = df.columns[:6].to_list() + [df.columns[-1]] + df.columns[6:-1].to_list()
    df = df[col_order]

    return df

tmp = os.listdir("./data")[1]
df = pd.read_csv(f"./data/{tmp}", encoding="cp949", index_col=False, error_bad_lines=False)
df.info()
df[df=="종로2가사거리"]

df = preprocess_scheme1(df)
df.info()
[df[column].dtypes for column in df.columns[8:-1].to_list()]

df[]

df.columns
pd.__version__






.str.split()

df.loc[[0]]
df.loc[[0,1,2]]
#%%
import csv
with open(f"./data/{tmp}", "r", encoding="cp949") as f:
    reader = csv.reader(f, delimiter=";")
    headers = next(reader)
    headers2 = next(reader)

tmp = headers2[0].split(",")
([tmp[0], ''] + tmp[1:]).join(",")
tmp2 = ",".join([tmp[0], ''] + tmp[1:])

import re
pattern = "(*,*,*)"
rmve_bracket = "\(.*\)|\s-\s.*" 
re.sub(rmve_bracket, "(.)", tmp2)
