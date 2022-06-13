#%%
import os
import sys
import csv
import numpy as np
import pandas as pd
import re

# %%
def preprocess_scheme1(df):
    df = df.drop("등록일자", axis="columns")
    df["버스정류장ARS번호"] = df["버스정류장ARS번호"].replace("~", 0).astype("int64")
    df["버스정류장ARS번호_Text"] = df["버스정류장ARS번호"].astype("string").str.pad(width=5, side="left", fillchar="0")
    col_order = df.columns[:6].to_list() + [df.columns[-1]] + df.columns[6:-1].to_list()
    df = df[col_order]

    return df

tmp = os.listdir("./data")[-3]
tmp = os.listdir("./data")[2]
tmp = clean_file(tmp)
df = pd.read_csv(f"./data/{tmp}", encoding="utf-8-sig", index_col=False)
df.info()

df = preprocess_scheme1(df)
df.info()
[df[column].dtypes for column in df.columns[8:-1].to_list()]




#%%
def clean_file(dirty_file):
    file_name = f"/modified_{dirty_file}"

    with open(f"./data/{file_name}", "w", encoding="utf-8-sig", newline="") as csvfile:
        row_writer = csv.writer(csvfile, delimiter=',')

        with open(f"./data/{tmp}", "r", encoding="cp949") as f:
            readers = csv.reader(f, delimiter=";")
            for step, reader in enumerate(readers):
                row = reader[0].split(",")
                if step != 0: 
                    row = ",".join([row[0], ''] + row[1:])
                    row = re.sub(r'\([^()]+\)', lambda x: x.group(0).replace(",", "."), row)
                    row = re.sub(r"[가-힣]\,[가-힣]", lambda x: x.group(0).replace(",", "."), row)
                    row = row.split(",")
                row_writer.writerow(row)

    return file_name

#%%
