import requests
import pandas as pd
from tqdm import tqdm


def extract_region_names(x, y, REST_API_KEY="48ecd349e2c5e3c5a48493ff45ac97b5"):
    url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={x}&y={y}"
    header = {"Authorization": f"KakaoAK {REST_API_KEY}"}
    response = requests.post(url, headers=header)
    contents = eval(response.text)

    region2 = contents["documents"][1]["region_2depth_name"]
    region3 = contents["documents"][1]["region_3depth_name"]

    return region2, region3


def fetch_businfo(data_dir):
    bus_info_dir = f"{data_dir}/20220429기준_서울시정류소리스트.csv"
    df = pd.read_csv(bus_info_dir)
    region2_lst, region3_lst = [], []

    for i in tqdm(range(len(df))):
        x, y = df["좌표X"][i], df["좌표Y"][i]
        region2, region3 = extract_region_names(x, y)
        region2_lst.append(region2)
        region3_lst.append(region3)

    df.insert(5, "구명칭", region2_lst, allow_duplicates=True)
    df.insert(6, "동명칭", region3_lst, allow_duplicates=True)

    return df
