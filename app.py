
import streamlit as st
import json
import os
from datetime import date

DATA_FILE = "progress.json"

monthly_plan = {
    "June": {
        "Learning Goals": [
            "✅ Finish CS50P course",
            "✅ Learn SQL basics (Kaggle/W3Schools)",
            "✅ Practice pandas / matplotlib / seaborn"
        ],
        "Project": [
            "📊 Analyze UCI student performance dataset",
            "🔍 Identify factors affecting grades",
            "📝 Write report (Markdown or PDF)"
        ]
    },
    "July": {
        "Learning Goals": [
            "✅ Advance pandas (groupby, pivot, merge)",
            "✅ Learn Plotly / seaborn for interactive charts",
            "✅ Practice analytical report writing"
        ],
        "Project": [
            "🛍 Analyze e-commerce or user behavior data",
            "📈 Visualize patterns (bestselling, peak time)",
            "📑 Output structured report with notebook"
        ]
    },
    "August": {
        "Learning Goals": [
            "✅ Finish Kaggle Intro & Intermediate ML",
            "✅ Understand train/test split, accuracy, overfitting"
        ],
        "Project": [
            "🥊 Predict UFC win/loss using fighter stats",
            "🧠 Feature engineering + model training",
            "📊 Evaluate with accuracy & confusion matrix"
        ]
    }
}

def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

st.title("📘 3-Month Data Analysis Study Plan")

month = st.selectbox("Select Month", list(monthly_plan.keys()))
progress = load_progress()
if month not in progress:
    progress[month] = {}

for section, tasks in monthly_plan[month].items():
    st.subheader(section)
    if section not in progress[month]:
        progress[month][section] = {}
    for task in tasks:
        default = progress[month][section].get(task, {}).get("done", False)
        checked = st.checkbox(task, value=default, key=month + section + task)
        if checked:
            progress[month][section][task] = {
                "done": True,
                "timestamp": progress[month][section].get(task, {}).get("timestamp") or str(date.today())
            }
        else:
            progress[month][section][task] = {"done": False, "timestamp": ""}

save_progress(progress)

# 统计进度
total = sum(len(t) for s, t in monthly_plan[month].items())
done = sum(1 for s in progress[month].values() for t in s.values() if t.get("done"))
st.progress(done / total)
st.caption(f"Progress: {done}/{total} tasks completed")
