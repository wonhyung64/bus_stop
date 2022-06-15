#%%
import os
import pandas as pd
from utils import (
    fetch_scheme1,
    fetch_scheme2,
    fetch_businfo,
)

if __name__ == "__main__":
    data_dir = "./data"
    encoding = "cp949"
    df_scheme1_dir = f"{data_dir}/정류소별 승차정보_01파일.csv"
    df_scheme2_dir = f"{data_dir}/정류소별 승차정보_02파일.csv"
    df_businfo_dir = f"{data_dir}/버스위치정보.csv"

    if not (os.path.exists(df_scheme1_dir)):
        df_scheme1 = fetch_scheme1(data_dir, encoding)
        df_scheme1.to_csv(df_scheme1_dir, index=False)
    else:
        df_scheme1 = pd.read_csv(df_scheme1_dir)

    if not (os.path.exists(df_scheme2_dir)):
        df_scheme2 = fetch_scheme2(df_scheme1)
        df_scheme2.to_csv(df_scheme2_dir, index=False)
    else:
        df_scheme2 = pd.read_csv(df_scheme2_dir)

    if not (os.path.exists(df_businfo_dir)):
        df_businfo = fetch_businfo(data_dir)
        df_businfo.to_csv(df_businfo_dir, index=False)
    else:
        df_businfo = pd.read_csv(df_businfo_dir)

    df_businfo = df_businfo[["ARS-ID", "구명칭", "동명칭"]]
    df_businfo.columns = ["버스정류장ARS번호", "구명칭", "동명칭"]

    df_scheme1 = pd.merge(df_scheme1, df_businfo, how="left")
    df_scheme1["버스정류장ARS번호_Text"] = (
        df_scheme1["버스정류장ARS번호"]
        .astype("string")
        .str.pad(width=5, side="left", fillchar="0")
    )
    df_scheme1.to_csv(df_scheme1_dir, index=False)

    df_scheme2 = pd.merge(df_scheme2, df_businfo, how="left")
    df_scheme2["버스정류장ARS번호_Text"] = (
        df_scheme2["버스정류장ARS번호"]
        .astype("string")
        .str.pad(width=5, side="left", fillchar="0")
    )
    df_scheme2.to_csv(df_scheme2_dir, index=False)
