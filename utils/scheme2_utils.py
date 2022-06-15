import pandas as pd
from tqdm import tqdm


def fetch_scheme2(df_scheme1):
    row_scheme2 = []
    for i in tqdm(range(len(df_scheme1))):
        row_scheme1 = df_scheme1.iloc[i, :].to_dict()
        for hour in range(0, 24):
            new_col = {
                "사용년월": row_scheme1["사용년월"],
                "노선ID": row_scheme1["노선ID"],
                "노선번호": row_scheme1["노선번호"],
                "노선명": row_scheme1["노선명"],
                "표준버스정류장ID": row_scheme1["표준버스정류장ID"],
                "버스정류장ARS번호": row_scheme1["버스정류장ARS번호"],
                "버스정류장ARS번호_Text": row_scheme1["버스정류장ARS번호_Text"],
                "역명": row_scheme1["역명"],
                "시간대": f"{str(hour):0>2}",
                "승차승객수": row_scheme1[f"{str(hour):0>2}시승차총승객수"],
                "하차승객수": row_scheme1[f"{str(hour):0>2}시하차총승객수"],
            }
            row_scheme2.append(new_col)

    df_scheme2 = pd.DataFrame(row_scheme2)

    return df_scheme2
