import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac支援中文的字體
plt.rcParams['axes.unicode_minus'] = False


# 輸出資料夾存在
os.makedirs("charts", exist_ok=True)

# 讀取資料
df = pd.read_csv("input_data/行動寬頻用戶每月平均數據用量.csv")
df.columns = df.columns.str.strip()

df["year"] = df["年月"].astype(str).str.split("/").str[0].astype(int)
df["month"] = df["年月"].astype(str).str.split("/").str[1].astype(int)

# 108~114
df = df[(df["year"] >= 108) & (df["year"] <= 114)]

# 年度總流量
yearly = df.groupby("year")["平均每一用戶數據傳輸量（GBytes）"].mean()

plt.figure(figsize=(10, 6))
plt.plot(yearly.index, yearly.values, marker='o')
plt.title("108–114 年行動數據平均用量趨勢")
plt.xlabel("年度")
plt.ylabel("平均用量（GB）")
plt.grid(True)
plt.savefig("charts/yearly_trend.png", dpi=120)
plt.close()

print("已輸出：charts/yearly_trend.png")

# 年度比較
operator_yearly = df.groupby(["year", "業者名稱"])["平均每一用戶數據傳輸量（GBytes）"].mean().unstack()

operator_yearly.plot(figsize=(12, 6), marker='o')
plt.legend(title="業者名稱", fontsize=9, title_fontsize=10, loc="upper left", ncol=2)
plt.title("各電信業者 108–114 年平均用量比較")
plt.xlabel("年度")
plt.ylabel("平均用量（GB）")
plt.grid(True)
plt.savefig("charts/operator_comparison.png", dpi=120)
plt.close()

print("已輸出：charts/operator_comparison.png")


mapping = {
    "中華電信股份有限公司": "中華電信",
    "台灣大哥大股份有限公司": "台灣大哥大",
    "遠傳電信股份有限公司": "遠傳電信",
    "台灣之星電信股份有限公司": "台灣之星",
    "亞太電信股份有限公司": "亞太電信",
}

df["業者名稱"] = df["業者名稱"].replace(mapping)

# 季節性趨勢
season = df.groupby("month")["平均每一用戶數據傳輸量（GBytes）"].mean()

plt.figure(figsize=(10, 6))
plt.plot(season.index, season.values, marker='o')
plt.title("台灣行動數據月度季節性趨勢（108–114 平均）")
plt.xlabel("月份")
plt.ylabel("平均用量（GB）")
plt.grid(True)
plt.savefig("charts/seasonality.png", dpi=120)
plt.close()

print("已輸出：charts/seasonality.png")
