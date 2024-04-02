import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Initialize Streamlit app
st.set_page_config(page_title="Enhanced To-Do List")

# UI
st.title("***Enhanced To-Do List Manager***")
st.subheader("Organize, Prioritize, and Manage your tasks effectively!")

# Local Database
@st.cache(allow_output_mutation=True)
def get_local_data():
    return pd.DataFrame(columns=["Task", "Category", "Due Date", "Priority", "Completed"])

data = get_local_data()

# Functions for interacting with local data
def save_local_data():
    data.to_csv("local_data.csv", index=False)

def load_local_data():
    return pd.read_csv("local_data.csv") if "local_data.csv" in os.listdir() else pd.DataFrame(columns=["Task", "Category", "Due Date", "Priority", "Completed"])

def add_task(task, category, due_date, priority):
    global data
    new_task = {"Task": task, "Category": category, "Due Date": due_date, "Priority": priority, "Completed": False}
    data = data.append(new_task, ignore_index=True)
    save_local_data()

def edit_task(task_id, updated_task, updated_category, updated_due_date, updated_priority, completed):
    global data
    task_index = data[data.index == task_id].index[0]
    data.at[task_index, "Task"] = updated_task
    data.at[task_index, "Category"] = updated_category
    data.at[task_index, "Due Date"] = updated_due_date
    data.at[task_index, "Priority"] = updated_priority
    data.at[task_index, "Completed"] = completed
    save_local_data()

def delete_task(task_id):
    global data
    data = data.drop(index=task_id).reset_index(drop=True)
    save_local_data()

# Load data from CSV
load_local_data()

# Add example to-do list tasks
example_tasks = [
    {"Task": "Start my business",
     "Category": "Business",
     "Due Date": "2024-04-15",
     "Priority": "High",
     "Completed": False},
    {"Task": "Apply for a grant",
     "Category": "Finance",
     "Due Date": "2024-03-30",
     "Priority": "Medium",
     "Completed": False},
    {"Task": "Fix my credit",
     "Category": "Finance",
     "Due Date": "2024-04-10",
     "Priority": "High",
     "Completed": False},
    {"Task": "Market on social media",
     "Category": "Marketing",
     "Due Date": "2024-04-05",
     "Priority": "High",
     "Completed": False},
    {"Task": "Daily habit tracker",
     "Category": "Personal Development",
     "Due Date": "",
     "Priority": "Low",
     "Completed": False}
]

# Display tasks with additional features
for task_data in example_tasks:
    st.subheader(task_data["Task"])
    st.write(f"- Category: {task_data['Category']}")
    st.write(f"- Due Date: {task_data['Due Date']}")
    st.write(f"- Priority: {task_data['Priority']}")
    task_id = st.empty().id
    completed = st.session_state.get(f"completed_{task_id}", False)
    completed = st.checkbox("Completed", key=f"completed_{task_id}", value=completed)
    if st.button("Edit Task", key=f"edit_{task_id}"):
        updated_task = st.text_input("Task", value=task_data["Task"])
        updated_category = st.text_input("Category", value=task_data["Category"])
        updated_due_date = st.date_input("Due Date", value=datetime.strptime(task_data["Due Date"], "%Y-%m-%d") if task_data["Due Date"] else "")
        updated_priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task_data["Priority"]))
        edit_task(task_id, updated_task, updated_category, updated_due_date.strftime("%Y-%m-%d") if updated_due_date else "", updated_priority, completed)
    if st.button("Delete Task", key=f"delete_{task_id}"):
        delete_task(task_id)
    st.write("---")

# Add Task Section
st.subheader("Add New Task")
new_task = st.text_input("Task")
new_category = st.text_input("Category")
new_due_date = st.date_input("Due Date")
new_priority = st.selectbox("Priority", options=["Low", "Medium", "High"])
if st.button("Add Task", key="add_new_task", disabled=not new_task):
    add_task(new_task, new_category, new_due_date.strftime("%Y-%m-%d") if new_due_date else "", new_priority)

# Sorting and Filtering
st.subheader("Sorting and Filtering Options")
sort_by = st.selectbox("Sort By", options=["Due Date", "Priority", "Category"])
filter_category = st.selectbox("Filter by Category", options=["All"] + data["Category"].unique().tolist())
filter_completed = st.checkbox("Show Completed Tasks")
filtered_tasks = data.copy()
if filter_category != "All":
    filtered_tasks = filtered_tasks[filtered_tasks["Category"] == filter_category]
if not filter_completed:
    filtered_tasks = filtered_tasks[filtered_tasks["Completed"] == False]
if sort_by == "Due Date":
    filtered_tasks = filtered_tasks.sort_values(by=["Due Date"])
elif sort_by == "Priority":
    filtered_tasks = filtered_tasks.sort_values(by=["Priority"])

st.write(filtered_tasks)
