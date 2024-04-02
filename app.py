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
def get_local_data():
    return pd.DataFrame(columns=["Task", "Category", "Due Date", "Priority", "Completed", "Subtasks"])

data = st.cache(get_local_data)()

# Functions for interacting with local data
def save_local_data():
    data.to_csv("local_data.csv", index=False)

def load_local_data():
    return pd.read_csv("local_data.csv") if "local_data.csv" in os.listdir() else pd.DataFrame(columns=["Task", "Category", "Due Date", "Priority", "Completed", "Subtasks"])

def add_task(task, category, due_date, priority, subtasks):
    global data
    new_task = {"Task": task, "Category": category, "Due Date": due_date, "Priority": priority, "Completed": False, "Subtasks": subtasks}
    data = data.append(new_task, ignore_index=True)
    save_local_data()

def edit_task(task_id, updated_task, updated_category, updated_due_date, updated_priority, completed, updated_subtasks):
    global data
    data.at[task_id, "Task"] = updated_task
    data.at[task_id, "Category"] = updated_category
    data.at[task_id, "Due Date"] = updated_due_date
    data.at[task_id, "Priority"] = updated_priority
    data.at[task_id, "Completed"] = completed
    data.at[task_id, "Subtasks"] = updated_subtasks
    save_local_data()

def delete_task(task_id):
    global data
    data = data.drop(index=task_id).reset_index(drop=True)
    save_local_data()

# Load data from CSV
load_local_data()

# Add example to-do list tasks with subtasks
example_tasks = [
    {"Task": "Start my business",
     "Category": "Business",
     "Due Date": "2024-04-15",
     "Priority": "High",
     "Completed": False,
     "Subtasks": ["Create business plan", "Register business name", "Design logo", "Set up website", "Open business bank account"]},
    {"Task": "Apply for a grant",
     "Category": "Finance",
     "Due Date": "2024-03-30",
     "Priority": "Medium",
     "Completed": False,
     "Subtasks": ["Research grant options", "Gather necessary documents", "Fill out application form", "Submit application", "Follow up on application status"]},
    {"Task": "Fix my credit",
     "Category": "Finance",
     "Due Date": "2024-04-10",
     "Priority": "High",
     "Completed": False,
     "Subtasks": ["Obtain credit report", "Dispute errors on credit report", "Pay off outstanding debts", "Reduce credit card balances", "Monitor credit score"]},
    {"Task": "Market on social media",
     "Category": "Marketing",
     "Due Date": "2024-04-05",
     "Priority": "High",
     "Completed": False,
     "Subtasks": ["Create content calendar", "Post regularly on social media platforms", "Engage with followers", "Run targeted ads", "Analyze social media metrics"]},
    {"Task": "Daily habit tracker",
     "Category": "Personal Development",
     "Due Date": "",
     "Priority": "Low",
     "Completed": False,
     "Subtasks": ["Exercise for 30 minutes", "Read for 20 minutes", "Meditate for 10 minutes", "Journal for 15 minutes", "Review daily goals"]}
]

# Display tasks with additional features
for task_id, task_data in enumerate(example_tasks):
    task_key = f"task-{task_id}"
    st.subheader(task_data["Task"])
    st.write(f"- Category: {task_data['Category']}")
    st.write(f"- Due Date: {task_data['Due Date']}")
    st.write(f"- Priority: {task_data['Priority']}")
    st.write("- Subtasks:")
    for subtask_id, subtask in enumerate(task_data["Subtasks"]):
        st.write(f"  - {subtask}")
    completed = st.checkbox("Completed")
    if st.button("Edit Task"):
        updated_task = st.text_input("Task", value=task_data["Task"])
        updated_category = st.text_input("Category", value=task_data["Category"])
        updated_due_date = st.date_input("Due Date", value=datetime.strptime(task_data["Due Date"], "%Y-%m-%d") if task_data["Due Date"] else "")
        updated_priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task_data["Priority"]))
        updated_subtasks = st.text_area("Subtasks", value="\n".join(task_data["Subtasks"]))
        edit_task(task_id, updated_task, updated_category, updated_due_date, updated_priority, completed, updated_subtasks.split("\n"))

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select a feature",
    ["Create Flashcard", "Create Appointment", "Set Goals", "Create Social Post", "Quote of the Day", "Upload Image", "View Dashboard"]
)

# Main content based on user selection
if page == "Create Flashcard":
    create_flashcard()
elif page == "Create Appointment":
    create_appointment()
elif page == "Set Goals":
    set_goals()
elif page == "Create Social Post":
    create_social_post()
elif page == "Quote of the Day":
    quote_of_the_day()
elif page == "Upload Image":
    upload_image()
elif page == "View Dashboard":
    view_dashboard()
