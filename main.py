#%%
from tkinter.tix import COLUMN
import matplotlib.pyplot as plt
import pandas as pd
from utils import (
    plugin_neptune,
    NEPTUNE_API_KEY,
    NEPTUNE_PROJECT,
    load_df,
    mk_periods,
    test_covid_effect,
    test_shelter_effect,
    load_shelters_lst,
    extract_mean_pair,
)

#%%
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


def construct_pop_info():
    df1 = pd.read_csv("C:/Users/USER/Downloads/분기별세대수.csv", encoding="cp949")
    df2 = pd.read_csv("C:/Users/USER/Downloads/월별세대수.csv", encoding="cp949")
    df_merged = df2.merge(df1, how="right", on=["main_address", "sub_address", "항목"])
    df_org = df_merged.copy()

    df_pop = pd.DataFrame(columns=df_org.columns)
    for i in range(len(df_org)):
        try:
            num = int(df_merged.iloc[i,2][:-3])
        except:
            num = int(df_merged.iloc[i,2][:-6])
        new_row = pd.concat([df_merged.iloc[i,:3], df_merged.iloc[i,3:] * num])
        df_pop = df_pop.append(new_row)
    new_cols = [col + "_인구" for col in df_pop.columns.tolist()]
    df_pop.columns = new_cols
    
    df_base = df_merged.iloc[:,:3]
    for i in range(3,33):
        df_base = pd.concat([df_base, df_merged.iloc[:,i]], axis=1)
        df_base = pd.concat([df_base, df_pop.iloc[:,i]], axis=1)
    df_base.to_csv("C:/Users/USER/Downloads/주민수정보파일.csv", encoding="cp949", index=False)


def EDA(data_dir, smpl_SeungDong, periods, bool_shelter):
    for num, (per_bef, per_aft, build_day) in enumerate(periods):
        if bool_shelter: 
            str_shelter = "쉼터O"
            int_shelter = 2
            shelters = load_shelters_lst(data_dir, f"스마트쉼터_{build_day}")
            shelter_smpl = smpl_SeungDong[smpl_SeungDong["버스정류장ARS번호_Text"].isin(shelters)]
        else: 
            str_shelter = "쉼터X"
            int_shelter = 1
            no_shelters_lst = load_shelters_lst(data_dir, "스마트쉼터")
            shelter_smpl = smpl_SeungDong[
                ~smpl_SeungDong["버스정류장ARS번호_Text"].isin(no_shelters_lst)
            ]

        mu_1, mu_2 = extract_mean_pair(shelter_smpl, per_bef, per_aft)
        stats1 = pd.Series(mu_1).describe().to_frame(
            name=f"{per_bef[0][:4]}.{per_bef[0][4:6]}-{per_bef[1][:4]}.{per_bef[1][4:6]}"
            )
        stats2 = pd.Series(mu_2).describe().to_frame(
            name=f"{per_aft[0][:4]}.{per_aft[0][4:6]}-{per_aft[1][:4]}.{per_aft[1][4:6]}"
            )
        stats = pd.concat([stats1, stats2], axis=1)
        stats.to_csv(f"C:/Users/USER/Documents/GitHub/bus_stop/data/res/eda{int_shelter}_{num+1}.csv", index=True)
        n = len(mu_1)
        draw_boxplot(mu_1, mu_2, build_day, per_bef, per_aft, str_shelter, n)


def draw_boxplot(mu_1, mu_2, build_day, per_bef, per_aft, str_shelter, n):
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (5, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = "Malgun Gothic"

    fig, ax = plt.subplots()

    ax.boxplot([mu_1, mu_2])
    ax.set_title(f"성동구 {build_day[:4]}.{build_day[4:6]}.{build_day[6:]} 기준 ({str_shelter}, n={n})")
    ax.set_xticks(ticks=[1,2], labels=[
        f"{per_bef[0][:4]}.{per_bef[0][4:6]}-{per_bef[1][:4]}.{per_bef[1][4:6]}",
        f"{per_aft[0][:4]}.{per_aft[0][4:6]}-{per_aft[1][:4]}.{per_aft[1][4:6]}",
        ])
    ax.set_ylabel('평균     \n승객     \n수     \n(천명)     ', loc="center", rotation="horizontal")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    

def format_func(value, tick_number):
    return value / 1000


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
    smpl_SeungDong = df[df["구명칭"] == "성동구"]
    periods = mk_periods()
    EDA(data_dir, smpl_SeungDong, periods, bool_shelter=False)
    
