#%%
import os
import openpyxl
import pandas as pd
from utils import (
    fetch_scheme1,
    fetch_scheme2,
    fetch_businfo,
)

def load_df(data_dir, encoding, df_scheme1_dir, df_scheme2_dir, df_businfo_dir):
    if not(os.path.exists(f"{df_scheme1_dir}_merged.csv")) or not(os.path.exists(f"{df_scheme2_dir}_merged.csv")):

        if not (os.path.exists(f"{df_scheme1_dir}.csv")):
            df_scheme1 = fetch_scheme1(data_dir, encoding)
            df_scheme1.to_csv(f"{df_scheme1_dir}.csv", index=False)
        else:
            df_scheme1 = pd.read_csv(f"{df_scheme1_dir}.csv")

        if not (os.path.exists(f"{df_scheme2_dir}.csv")):
            df_scheme2 = fetch_scheme2(df_scheme1)
            df_scheme2.to_csv(f"{df_scheme2_dir}.csv", index=False)
        else:
            df_scheme2 = pd.read_csv(f"{df_scheme2_dir}.csv")

        if not (os.path.exists(f"{df_businfo_dir}.csv")):
            df_businfo = fetch_businfo(data_dir)
            df_businfo.to_csv(f"{df_businfo_dir}.csv", index=False)
        else:
            df_businfo = pd.read_csv(f"{df_businfo_dir}.csv")

        df_businfo = df_businfo[["ARS-ID", "구명칭", "동명칭"]]
        df_businfo.columns = ["버스정류장ARS번호", "구명칭", "동명칭"]

        df_scheme1 = pd.merge(df_scheme1, df_businfo, how="left")
        df_scheme1.to_csv(f"{df_scheme1_dir}_merged.csv", index=False)

        df_scheme2 = pd.merge(df_scheme2, df_businfo, how="left")
        df_scheme2.to_csv(f"{df_scheme2_dir}_merged.csv", index=False)

    else:
        df_scheme1 = pd.read_csv(f"{df_scheme1_dir}_merged.csv")
        # df_scheme2 = pd.read_csv(f"{df_scheme2_dir}_merged.csv")

    return df_scheme1

#%%
if __name__ == "__main__":
    data_dir = "./data"
    encoding = "cp949"
    df_scheme1_dir = f"{data_dir}/정류소별 승차정보_01파일"
    df_scheme2_dir = f"{data_dir}/정류소별 승차정보_02파일"
    df_businfo_dir = f"{data_dir}/버스위치정보"
    df = load_df(data_dir, encoding, df_scheme1_dir, df_scheme2_dir, df_businfo_dir)
    
    df["버스정류장ARS번호_Text"] = (
        df["버스정류장ARS번호"].astype("string").str.pad(width=5, side="left", fillchar="0")
    )
    smpl_tmp = df[df["구명칭"] == "성동구"]

    rest_lst_dir = f"{data_dir}/스마트쉼터.xlsx"
    rest_lst = pd.read_excel(rest_lst_dir, header=None)[0].to_list()
    rest_lst = [f"{string:0>5}" for string in rest_lst]
    
    smpl = smpl_tmp[~smpl_tmp["버스정류장ARS번호_Text"].isin(rest_lst)]
    
    smpl_group = smpl.groupby(["사용년월", "버스정류장ARS번호_Text"], as_index=False).sum()
    smpl_group["총승차승객수"] = sum([smpl_group.iloc[:,i] for i in range(4,29) if i % 2 ==0])
    smpl_group = smpl_group[["사용년월", "버스정류장ARS번호_Text", "총승차승객수"]]
    smpl_rc = smpl_group.pivot(index="버스정류장ARS번호_Text", columns="사용년월", values="총승차승객수")
    smpl_rc = smpl_rc.dropna()
    smpl_rc


# %%
