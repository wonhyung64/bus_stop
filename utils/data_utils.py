import os
import pandas as pd
import openpyxl
from .scheme1_utils import fetch_scheme1
from .scheme2_utils import fetch_scheme2
from .businfo_utils import fetch_businfo


def load_df(data_dir, encoding, df_scheme1_dir, df_scheme2_dir, df_businfo_dir):
    if not (os.path.exists(f"{df_scheme1_dir}_merged.csv")) or not (
        os.path.exists(f"{df_scheme2_dir}_merged.csv")
    ):

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

    return df_scheme1


def mk_periods():
    per1_bef = ["201908", "202007"]
    per1_aft = ["202008", "202107"]

    per2_bef = ["202001", "202012"]
    per2_aft = ["202101", "202112"]

    per3_bef = ["202008", "202105"]
    per3_aft = ["202108", "202205"]

    per4_bef = ["202101", "202105"]
    per4_aft = ["202201", "202205"]

    periods = [
        (per1_bef, per1_aft, "20200731"),
        (per2_bef, per2_aft, "20201218"),
        (per3_bef, per3_aft, "20210729"),
        (per4_bef, per4_aft, "20220107"),
    ]

    return periods
