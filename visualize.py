import pandas as pd
import matplotlib.pyplot as plt
import os

# 中文字體（Mac）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 輸出資料夾
os.makedirs("charts", exist_ok=True)

# 讀取第一個專案輸出的年度報表
year_folder = "output_by_year"

all_data = []

for file in os.listdir(year_folder):
    if file.endswith(".xlsx"):
        path = os.path.join(year_folder, file)
        df = pd.read_excel(path)
        all_data.append(df)

# 合併
df = pd.concat(all_data, ignore_index=True)

# 108–114 年度平均用量趨勢
yearly = df.groupby("year")["平均每一用戶數據傳輸量（GBytes）"].mean()

plt.figure(figsize=(10, 6))
plt.plot(yearly.index, yearly.values, marker='o')
plt.title("108–114 年行動數據平均用量趨勢（使用整理後資料）")
plt.xlabel("年度")
plt.ylabel("平均用量（GB）")
plt.grid(True)
plt.savefig("charts/yearly_trend.png", dpi=120)
plt.close()

print("已輸出：charts/yearly_trend.png")

# 各業者年度比較
operator_yearly = (
    df.groupby(["year", "業者名稱"])["平均每一用戶數據傳輸量（GBytes）"]
    .mean()
    .unstack()
)

operator_yearly.plot(figsize=(12, 6), marker='o')
plt.title("各電信業者 108–114 平均用量比較（使用整理後資料）")
plt.xlabel("年度")
plt.ylabel("平均用量（GB）")
plt.grid(True)
plt.legend(title="業者名稱", fontsize=9)
plt.savefig("charts/operator_comparison.png", dpi=120)
plt.close()

print("已輸出：charts/operator_comparison.png")

# 季節性分析（月度平均）
season = df.groupby("month")["平均每一用戶數據傳輸量（GBytes）"].mean()

plt.figure(figsize=(10, 6))
plt.plot(season.index, season.values, marker='o')
plt.title("台灣行動數據月度季節性趨勢（整理後資料）")
plt.xlabel("月份")
plt.ylabel("平均用量（GB）")
plt.grid(True)
plt.savefig("charts/seasonality.png", dpi=120)
plt.close()

print("已輸出：charts/seasonality.png")
