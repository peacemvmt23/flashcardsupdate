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
    task_index = data.index[task_id]
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
    task_key = f"task_{task_id}"
    st.subheader(task_data["Task"], key=task_key)
    st.write(f"- Category: {task_data['Category']}")
    st.write(f"- Due Date: {task_data['Due Date']}")
    st.write(f"- Priority: {task_data['Priority']}")
    st.write("- Subtasks:")
    for subtask in task_data["Subtasks"]:
        st.write(f"  - {subtask}")
    completed = st.checkbox("Completed", key=f"completed_{task_id}")
    if st.button("Edit Task", key=f"edit_button_{task_id}"):
        updated_task = st.text_input("Task", value=task_data["Task"], key=f"updated_task_{task_id}")
        updated_category = st.text_input("Category", value=task_data["Category"], key=f"updated_category_{task_id}")
        updated_due_date = st.date_input("Due Date", value=datetime.strptime(task_data["Due Date"], "%Y-%m-%d") if task_data["Due Date"] else "", key=f"updated_due_date_{task_id}")
        updated_priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task_data["Priority"]), key=f"updated_priority_{task_id}")
        updated_subtasks = st.text_area("Subtasks", value="\n".join(task_data["Subtasks"]), key=f"updated_subtasks_{task_id}")
        edit_task(task_id, updated_task, updated_category, updated_due_date, updated_priority, completed, updated_subtasks.split("\n"))

# Flashcards App
def create_flashcard():
    st.subheader("Create a Flashcard")

    # Get user input for card type (question or answer)
    card_type = st.radio("Select card type:", ["Question", "Answer"])

    # Get user input for card content
    card_content = st.text_area(f"Enter {card_type.lower()} content:")

    # Display flashcard content
    st.write(f"Your {card_type} Card:")
    st.write(card_content)

    # Save flashcard to data dictionary
    data["Flashcards"].append({"Type": card_type, "Content": card_content})

def create_appointment():
    st.subheader("Create an Appointment")

    # Get user input for appointment details
    date = st.date_input("Select date:")
    time = st.time_input("Select time:")
    title = st.text_input("Enter title:")
    description = st.text_area("Enter description:")

    # Display appointment details
    st.write("Your Appointment Details:")
    st.write(f"Date: {date}")
    st.write(f"Time: {time}")
    st.write(f"Title: {title}")
    st.write(f"Description: {description}")

    # Save appointment to data dictionary
    data["Appointments"].append({"Date": date, "Time": time, "Title": title, "Description": description})

def set_goals():
    st.subheader("Set Goals")

    # Get user input for goals
    goal = st.text_area("Enter your goal:")

    # Display goals
    st.write("Your Goals:")
    st.write(goal)

    # Save goal to data dictionary
    data["Goals"].append({"Goal": goal})

def create_social_post():
    st.subheader("Create a Social Post")

    # Get user input for social post
    post_content = st.text_area("Enter post content:")

    # Display social post
    st.write("Your Social Post:")
    st.write(post_content)

    # Save social post to data dictionary
    data["Social Posts"].append({"Content": post_content})

def quote_of_the_day():
    st.subheader("Quote of the Day")

    # Display a random quote
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs"
    ]
    quote = st.selectbox("Select a quote:", quotes)
    st.write(quote)

def upload_image():
    st.subheader("Upload Image")

    # Get user input for image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    # Display uploaded image
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

        # Save image to local directory
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

def write_to_csv():
    df = pd.DataFrame.from_dict({(i,j): data[i][j] for i in data.keys() for j in range(len(data[i]))}, orient='index')
    df.to_csv("flashcards_data.csv", index_label=['Category', 'Index'])

def view_dashboard():
    st.title("Dashboard")

    # Display thumbnails for all items
    for category, items in data.items():
        st.subheader(category)
        for idx, item in enumerate(items):
            if category == "Flashcards":
                st.write(f"Flashcard {idx+1}: {item['Content']}")
            elif category == "Appointments":
                st.write(f"Appointment {idx+1}: {item['Title']}")
            elif category == "Goals":
                st.write(f"Goal {idx+1}: {item['Goal']}")
            elif category == "Social Posts":
                st.write(f"Social Post {idx+1}: {item['Content']}")

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
