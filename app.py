
import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="June Study Tracker", page_icon="🎮", layout="centered")

st.title("📆 2025年6月 RPG化学习任务打卡表")

# 加载每日任务数据
@st.cache_data
def load_data():
    data = [
        {"date": "2025-06-01", "phase": "CS50P Review + Shorts", "main": "完成CS50P Week9视频", "side": "练习class/property"},
        {"date": "2025-06-02", "phase": "CS50P Review + Shorts", "main": "观看Shorts并做笔记", "side": "回顾之前代码"},
        {"date": "2025-06-03", "phase": "CS50P Review + Shorts", "main": "挑选Final项目方向", "side": "整理CS50P Markdown"},
    ]
    # 自动生成 6/4 - 6/30（已压缩逻辑简写）
    from datetime import timedelta
    base_date = datetime.strptime("2025-06-04", "%Y-%m-%d")
    for i in range(27):
        d = base_date + timedelta(days=i)
        day = d.day
        if day <= 7:
            phase = "CS50P Review + Shorts"
            main = ["完成CS50P Week9视频", "观看Shorts并做笔记", "挑选Final项目方向"][i % 3]
            side = ["练习class/property", "回顾之前代码", "整理CS50P Markdown"][i % 3]
        elif day <= 14:
            phase = "SQL 基础学习"
            main = ["学习SELECT语句", "GROUP BY与聚合", "练习JOIN与子查询"][i % 3]
            side = ["使用CS50 IDE练习", "总结SQL语法", "做一个SQL小练习"][i % 3]
        elif day <= 21:
            phase = "UCI项目分析实战"
            main = ["加载student数据", "分析字段特征", "绘图+初步结论"][i % 3]
            side = ["写Markdown记录", "画heatmap", "计算相关性系数"][i % 3]
        else:
            phase = "项目收尾"
            main = ["撰写分析总结", "整理Notebook", "上传到GitHub"][i % 3]
            side = ["写结论段", "封面页美化", "发给朋友请教反馈"][i % 3]
        data.append({
            "date": d.strftime("%Y-%m-%d"),
            "phase": phase,
            "main": main,
            "side": side
        })
    return pd.DataFrame(data)

df = load_data()
today = datetime.now().strftime("%Y-%m-%d")
today_tasks = df[df["date"] == today]

if today_tasks.empty:
    st.info("🎉 今天不是 6 月学习日程内的一天，或你已完成所有任务！")
else:
    row = today_tasks.iloc[0]
    st.subheader(f"📅 今天是：{row['date']} - {row['phase']}")
    st.write(f"🎯 主线任务：{row['main']}")
    st.write(f"🧩 支线任务：{row['side']}")

    # 加载或保存进度
    try:
        with open("progress.json", "r") as f:
            progress = json.load(f)
    except:
        progress = {}

    done = progress.get(row["date"], False)
    checked = st.checkbox("✅ 我已完成今天的任务", value=done)

    if checked and not done:
        progress[row["date"]] = True
        with open("progress.json", "w") as f:
            json.dump(progress, f)
        st.success("打卡成功！XP +10 🎉")

    # 显示总进度
    total = len(df)
    finished = sum(1 for v in progress.values() if v)
    st.progress(finished / total)
    st.caption(f"⭐ 当前进度：{finished}/{total} 天已完成")
