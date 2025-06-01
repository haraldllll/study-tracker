
import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="RPG打卡中心", page_icon="📆", layout="centered")
st.title("🎮 暑期学习 RPG 打卡系统（6–8月）")

# 月份选择器
month = st.selectbox("📅 选择学习月份", ["6月", "7月", "8月"])
month_map = {"6月": 6, "7月": 7, "8月": 8}
month_num = month_map[month]

# 任务数据生成函数
@st.cache_data
def generate_tasks(month):
    task_list = []
    base_date = datetime(2025, month, 1)
    for i in range(30 if month != 8 else 31):  # 6,7月30天；8月31天
        d = base_date.replace(day=i+1)
        day = d.day
        if month == 6:
            if day <= 7:
                phase, main, side = "CS50P Review", "完成CS50P Week9视频", "整理CS50P笔记"
            elif day <= 14:
                phase, main, side = "SQL 学习", "掌握SELECT/WHERE", "写SQL练习"
            elif day <= 21:
                phase, main, side = "UCI分析项目", "分析字段分布", "画图初探"
            else:
                phase, main, side = "项目总结", "撰写报告", "上传GitHub"
        elif month == 7:
            if day <= 10:
                phase, main, side = "pandas进阶", "学习groupby+merge", "练习pivot_table"
            elif day <= 20:
                phase, main, side = "数据可视化", "制作交互图表", "熟练Plotly/seaborn"
            else:
                phase, main, side = "行为分析项目", "完成电商分析", "输出图文报告"
        else:  # 8月
            if day <= 10:
                phase, main, side = "ML入门", "学习train/test split", "理解过拟合"
            elif day <= 20:
                phase, main, side = "建模实战", "用随机森林建模", "做准确率评估"
            else:
                phase, main, side = "模型总结", "报告撰写+GitHub", "学习模型调参"
        task_list.append({
            "date": d.strftime("%Y-%m-%d"),
            "phase": phase,
            "main": main,
            "side": side
        })
    return pd.DataFrame(task_list)

df = generate_tasks(month_num)
today = datetime.now().strftime("%Y-%m-%d")
today_row = df[df["date"] == today]

if not today_row.empty:
    row = today_row.iloc[0]
    st.subheader(f"📅 今天：{row['date']} - {row['phase']}")
    st.write(f"🎯 主线任务：{row['main']}")
    st.write(f"🧩 支线任务：{row['side']}")
else:
    st.info(f"🌙 当前选择的是 {month}，今天没有任务")

# 打卡进度管理
progress_file = f"progress_{month}.json"
try:
    with open(progress_file, "r") as f:
        progress = json.load(f)
except:
    progress = {}

# 今日任务打卡
if not today_row.empty:
    done = progress.get(today, False)
    checked = st.checkbox("✅ 今日任务完成", value=done)
    if checked and not done:
        progress[today] = True
        with open(progress_file, "w") as f:
            json.dump(progress, f)
        st.success("打卡成功！🎉")

# 总进度显示
total = len(df)
finished = sum(1 for v in progress.values() if v)
st.progress(finished / total)
st.caption(f"⭐ 当前进度：{finished}/{total} 天完成")
