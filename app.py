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
    return pd.DataFrame(columns=["Task", "Category", "Due Date", "Priority", "Completed", "Subtasks"])

data = get_local_data()

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
    task_index = task_id
    data.at[task_index, "Task"] = updated_task
    data.at[task_index, "Category"] = updated_category
    data.at[task_index, "Due Date"] = updated_due_date
    data.at[task_index, "Priority"] = updated_priority
    data.at[task_index, "Completed"] = completed
    data.at[task_index, "Subtasks"] = updated_subtasks
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
    st.subheader(task_data["Task"], key=task_key)
    st.write(f"- Category: {task_data['Category']}")
    st.write(f"- Due Date: {task_data['Due Date']}")
    st.write(f"- Priority: {task_data['Priority']}")
    st.write("- Subtasks:")
    for subtask_id, subtask in enumerate(task_data["Subtasks"]):
        subtask_key = f"{task_key}-subtask-{subtask_id}"
        st.write(f"  - {subtask}", key=subtask_key)
    completed = st.checkbox("Completed", key=f"{task_key}-completed")
    if st.button("Edit Task", key=f"{task_key}-edit"):
        updated_task = st.text_input("Task", value=task_data["Task"], key=f"{task_key}-input")
        updated_category = st.text_input("Category", value=task_data["Category"], key=f"{task_key}-category")
        updated_due_date = st.date_input("Due Date", value=datetime.strptime(task_data["Due Date"], "%Y-%m-%d") if task_data["Due Date"] else "", key=f"{task_key}-date")
        updated_priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task_data["Priority"]), key=f"{task_key}-priority")
        updated_subtasks = st.text_area("Subtasks", value="\n".join(task_data["Subtasks"]), key=f"{task_key}-subtasks")
        edit_task(task_id, updated_task, updated_category, updated_due_date, updated_priority, completed, updated_subtasks.split("\n"))

# Create Appointment Page
elif page == "Create Appointment":
    st.subheader("Create an Appointment")

    # Get user input for appointment details
    date = st.date_input("Select date:", key="date")
    time = st.time_input("Select time:", key="time")
    title = st.text_input("Enter title:", key="title")
    description = st.text_area("Enter description:", key="description")
    location = st.text_input("Enter location:", key="location")
    organizer = st.text_input("Enter organizer:", key="organizer")
    participants = st.text_input("Enter participants (comma-separated):", key="participants")
    reminder = st.checkbox("Set reminder", key="reminder")
    reminder_time = st.time_input("Reminder time:", key="reminder_time") if reminder else None
    reminder_date = st.date_input("Reminder date:", key="reminder_date") if reminder else None

    # Display appointment details
    st.write("Your Appointment Details:")
    st.write(f"Date: {date}")
    st.write(f"Time: {time}")
    st.write(f"Title: {title}")
    st.write(f"Description: {description}")
    st.write(f"Location: {location}")
    st.write(f"Organizer: {organizer}")
    st.write(f"Participants: {participants}")
    if reminder:
        st.write("Reminder Set:")
        st.write(f"Reminder Date: {reminder_date}")
        st.write(f"Reminder Time: {reminder_time}")

    # Save appointment to data dictionary
    data["Appointments"].append({
        "Date": date, 
        "Time": time, 
        "Title": title, 
        "Description": description, 
        "Location": location, 
        "Organizer": organizer, 
        "Participants": participants.split(','), 
        "Reminder": reminder, 
        "Reminder Time": reminder_time, 
        "Reminder Date": reminder_date
    })

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select a feature",
    ["Create Appointment", "View Dashboard"]
)
