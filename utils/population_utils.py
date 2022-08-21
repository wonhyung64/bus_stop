import pandas as pd


def construct_pop_info():
    df1 = pd.read_csv("C:/Users/USER/Downloads/분기별세대수.csv", encoding="cp949")
    df2 = pd.read_csv("C:/Users/USER/Downloads/월별세대수.csv", encoding="cp949")
    df_merged = df2.merge(df1, how="right", on=["main_address", "sub_address", "항목"])
    df_org = df_merged.copy()

    df_pop = pd.DataFrame(columns=df_org.columns)
    for i in range(len(df_org)):
        try:
            num = int(df_merged.iloc[i, 2][:-3])
        except:
            num = int(df_merged.iloc[i, 2][:-6])
        new_row = pd.concat([df_merged.iloc[i, :3], df_merged.iloc[i, 3:] * num])
        df_pop = df_pop.append(new_row)
    new_cols = [col + "_인구" for col in df_pop.columns.tolist()]
    df_pop.columns = new_cols

    df_base = df_merged.iloc[:, :3]
    for i in range(3, 33):
        df_base = pd.concat([df_base, df_merged.iloc[:, i]], axis=1)
        df_base = pd.concat([df_base, df_pop.iloc[:, i]], axis=1)
    df_base.to_csv("C:/Users/USER/Downloads/주민수정보파일.csv", encoding="cp949", index=False)
