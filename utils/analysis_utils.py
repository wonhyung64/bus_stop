import pandas as pd
import scipy.stats


def load_shelters_lst(data_dir, filename):
    shelters_dir = f"{data_dir}/{filename}.xlsx"
    shelters = pd.read_excel(shelters_dir, header=None)[0].to_list()
    shelters = [f"{string:0>5}" for string in shelters]

    return shelters


def extract_mean_pair(smpl, per_bef, per_aft):
    smpl_rc = recon_smpl(smpl, per_bef, per_aft)
    mu_1, mu_2 = calculate_mean(smpl_rc, per_bef, per_aft)

    return mu_1, mu_2


def paired_ttest(mu_1, mu_2):
    smpl_num = len(mu_1)
    res = scipy.stats.ttest_rel(mu_1, mu_2)

    return smpl_num, res


def wilcoxon_test(mu_1, mu_2):
    smpl_num = len(mu_1)
    res = scipy.stats.wilcoxon(
        mu_1, mu_2, zero_method="wilcox", correction=False, alternative="less"
    )

    return smpl_num, res


def recon_smpl(smpl, per_bef, per_aft):
    smpl_group = smpl.groupby(["사용년월", "버스정류장ARS번호_Text", "노선번호"], as_index=False).sum()
    smpl_group["총승차승객수"] = sum(
        [smpl_group.iloc[:, i] for i in range(5, 30) if i % 2 == 0]
    )
    smpl_group = smpl_group[["사용년월", "버스정류장ARS번호_Text", "노선번호", "총승차승객수"]]
    smpl_rc = (
        smpl_group.pivot(
            index=["버스정류장ARS번호_Text", "노선번호"], columns="사용년월", values="총승차승객수"
        ).loc[:, per_bef[0] : per_aft[1]]
    ).dropna()
    smpl_rc = smpl_rc.sum(axis=0, level=0)

    return smpl_rc


def calculate_mean(smpl_rc, per_bef, per_aft):
    smpl1 = smpl_rc.loc[:, per_bef[0] : per_bef[1]]
    smpl2 = smpl_rc.loc[:, per_aft[0] : per_aft[1]]
    mu_1 = smpl1.mean(axis=1).to_list()
    mu_2 = smpl2.mean(axis=1).to_list()

    return mu_1, mu_2


def test_covid_effect(data_dir, smpl_SeungDong, periods):
    no_shelters_lst = load_shelters_lst(data_dir, "스마트쉼터")
    no_shelter_smpl = smpl_SeungDong[
        ~smpl_SeungDong["버스정류장ARS번호_Text"].isin(no_shelters_lst)
    ]

    res_table = pd.DataFrame()
    for per_bef, per_aft, build_day in periods:
        mu_1, mu_2 = extract_mean_pair(no_shelter_smpl, per_bef, per_aft)
        smpl_num, res = paired_ttest(mu_1, mu_2)
        res_table = res_table.append(
            {
                "built_day": build_day,
                "per_bef": f"{per_bef[0]}-{per_bef[1]}",
                "per_aft": f"{per_aft[0]}-{per_aft[1]}",
                "sample #": smpl_num,
                "stats": res[0],
                "p-value": res[1],
            },
            ignore_index=True,
        )

    return res_table


def test_shelter_effect(data_dir, smpl_SeungDong, periods):
    res_table = pd.DataFrame()
    for per_bef, per_aft, build_day in periods:
        shelters = load_shelters_lst(data_dir, f"스마트쉼터_{build_day}")
        shelter_smpl = smpl_SeungDong[smpl_SeungDong["버스정류장ARS번호_Text"].isin(shelters)]
        mu_1, mu_2 = extract_mean_pair(shelter_smpl, per_bef, per_aft)
        smpl_num, res = wilcoxon_test(mu_1, mu_2)

        res_table = res_table.append(
            {
                "built_day": build_day,
                "per_bef": f"{per_bef[0]}-{per_bef[1]}",
                "per_aft": f"{per_aft[0]}-{per_aft[1]}",
                "sample #": smpl_num,
                "stats": res[0],
                "p_value": res[1],
            },
            ignore_index=True,
        )

    return res_table
