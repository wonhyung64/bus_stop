import pandas as pd
import matplotlib.pyplot as plt
from .analysis_utils import (
    load_shelters_lst,
    extract_mean_pair,
)


def eda(data_dir, smpl_SeungDong, periods, bool_shelter):
    for num, (per_bef, per_aft, build_day) in enumerate(periods):
        if bool_shelter:
            str_shelter = "쉼터O"
            int_shelter = 2
            shelters = load_shelters_lst(data_dir, f"스마트쉼터_{build_day}")
            shelter_smpl = smpl_SeungDong[
                smpl_SeungDong["버스정류장ARS번호_Text"].isin(shelters)
            ]
        else:
            str_shelter = "쉼터X"
            int_shelter = 1
            no_shelters_lst = load_shelters_lst(data_dir, "스마트쉼터")
            shelter_smpl = smpl_SeungDong[
                ~smpl_SeungDong["버스정류장ARS번호_Text"].isin(no_shelters_lst)
            ]

        mu_1, mu_2 = extract_mean_pair(shelter_smpl, per_bef, per_aft)
        stats1 = (
            pd.Series(mu_1)
            .describe()
            .to_frame(
                name=f"{per_bef[0][:4]}.{per_bef[0][4:6]}-{per_bef[1][:4]}.{per_bef[1][4:6]}"
            )
        )
        stats2 = (
            pd.Series(mu_2)
            .describe()
            .to_frame(
                name=f"{per_aft[0][:4]}.{per_aft[0][4:6]}-{per_aft[1][:4]}.{per_aft[1][4:6]}"
            )
        )
        stats = pd.concat([stats1, stats2], axis=1)
        stats.to_csv(
            f"C:/Users/USER/Documents/GitHub/bus_stop/data/res/eda{int_shelter}_{num+1}.csv",
            index=True,
        )
        n = len(mu_1)
        draw_boxplot(mu_1, mu_2, build_day, per_bef, per_aft, str_shelter, n)


def draw_boxplot(mu_1, mu_2, build_day, per_bef, per_aft, str_shelter, n):
    plt.style.use("default")
    plt.rcParams["figure.figsize"] = (5, 6)
    plt.rcParams["font.size"] = 10
    plt.rcParams["font.family"] = "Malgun Gothic"

    fig, ax = plt.subplots()

    ax.boxplot([mu_1, mu_2])
    ax.set_title(
        f"성동구 {build_day[:4]}.{build_day[4:6]}.{build_day[6:]} 기준 ({str_shelter}, n={n})"
    )
    ax.set_xticks(
        ticks=[1, 2],
        labels=[
            f"{per_bef[0][:4]}.{per_bef[0][4:6]}-{per_bef[1][:4]}.{per_bef[1][4:6]}",
            f"{per_aft[0][:4]}.{per_aft[0][4:6]}-{per_aft[1][:4]}.{per_aft[1][4:6]}",
        ],
    )
    ax.set_ylabel(
        "평균     \n승객     \n수     \n(천명)     ", loc="center", rotation="horizontal"
    )
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    plt.savefig("")


def format_func(value, tick_number):
    return value / 1000
