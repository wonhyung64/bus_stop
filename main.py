#%%
import pandas as pd
from utils import (
    plugin_neptune,
    NEPTUNE_API_KEY,
    NEPTUNE_PROJECT,
    load_df,
    mk_periods,
    test_covid_effect,
    test_shelter_effect,
)


def main():
    run = plugin_neptune(NEPTUNE_API_KEY, NEPTUNE_PROJECT)

    data_dir = "./data"
    encoding = "cp949"
    df_scheme1_dir = f"{data_dir}/정류소별 승차정보_01파일"
    df_scheme2_dir = f"{data_dir}/정류소별 승차정보_02파일"
    df_businfo_dir = f"{data_dir}/버스위치정보"
    df = load_df(data_dir, encoding, df_scheme1_dir, df_scheme2_dir, df_businfo_dir)
    df["버스정류장ARS번호_Text"] = (
        df["버스정류장ARS번호"].astype("string").str.pad(width=5, side="left", fillchar="0")
    )
    smpl_SeungDong = df[df["구명칭"] == "성동구"]
    periods = mk_periods()

    covid_table = test_covid_effect(data_dir, smpl_SeungDong, periods)
    shelter_table = test_shelter_effect(data_dir, smpl_SeungDong, periods)

    merged_table = covid_table.merge(
        shelter_table, how="inner", on=["설치시기", "설치 전 기간", "설치 후 기간"]
    )

    merged_table.to_csv(f"{data_dir}/result.csv", encoding="cp949", index=False)
    run["result"].upload(f"{data_dir}/result.csv")

    run.stop()


#%%
if __name__ == "__main__":
    main()
