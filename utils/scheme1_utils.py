import os
import tqdm
import csv
import re
import numpy as np
import pandas as pd


def fetch_scheme1(data_dir, encoding):
    file_names = os.listdir(data_dir)
    file_names.remove("20220429기준_서울시정류소리스트.csv")
    df_lst = []
    for i in tqdm(range(len(file_names))):
        file_name = file_names[i]
        try:
            df = pd.read_csv(
                f"{data_dir}/{file_name}", encoding="cp949", index_col=False
            )
            df = preprocess_scheme1(df)
        except:
            file_name = clean_file(file_name, encoding=encoding)
            df = pd.read_csv(
                f"{data_dir}/{file_name}", encoding=encoding, index_col=False
            )
            df = preprocess_scheme1(df)
        df_lst.append(df)
    df = pd.concat(df_lst, ignore_index=True)

    return df


def preprocess_scheme1(df):
    if len(df.columns) < 56:
        df["노선ID"] = np.nan
        col_order = [df.columns[0]] + [df.columns[-1]] + df.columns[1:-1].to_list()
        df = df[col_order]

    df["버스정류장ARS번호"] = df["버스정류장ARS번호"].replace("~", 0).astype("int64")
    df["버스정류장ARS번호_Text"] = (
        df["버스정류장ARS번호"].astype("string").str.pad(width=5, side="left", fillchar="0")
    )
    col_order = df.columns[:6].to_list() + [df.columns[-1]] + df.columns[6:-1].to_list()
    df = df[col_order]

    if len(df.columns) > 56:
        df = df.iloc[:, :56]
    columns1 = [
        "사용년월",
        "노선ID",
        "노선번호",
        "노선명",
        "표준버스정류장ID",
        "버스정류장ARS번호",
        "버스정류장ARS번호_Text",
        "역명",
    ]
    columns_tmp = [
        [f"{f'{time:0>2}'}시{state}차총승객수" for state in ("승", "하")]
        for time in range(0, 24)
    ]
    columns2 = []
    for i in range(len(columns_tmp)):
        columns2 += columns_tmp[i]
    columns_name = columns1 + columns2
    df.columns = columns_name

    return df


def clean_file(dirty_file, encoding):
    file_name = f"/modified_{dirty_file}"

    with open(f"./data/{file_name}", "w", encoding=encoding, newline="") as csvfile:
        row_writer = csv.writer(csvfile, delimiter=",")

        with open(f"./data/{dirty_file}", "r", encoding="cp949") as f:
            readers = csv.reader(f, delimiter=";")
            for step, reader in enumerate(readers):
                row = reader[0].split(",")
                if step != 0:
                    row = ",".join([row[0], ""] + row[1:])
                    row = re.sub(
                        r"\([^()]+\)", lambda x: x.group(0).replace(",", "."), row
                    )
                    row = re.sub(
                        r"[가-힣]\,[가-힣]", lambda x: x.group(0).replace(",", "."), row
                    )
                    row = re.sub(r"\,$", lambda x: x.group(0).replace(",", ""), row)
                    row = row.split(",")
                row_writer.writerow(row)

    return file_name
