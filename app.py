import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize data dictionary to store user inputs
data = {
    "Flashcards": [],
    "Appointments": [],
    "Goals": [],
    "Social Posts": []
}

# Function to create flashcards
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

# Function to create appointments
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

# Function to set goals
def set_goals():
    st.subheader("Set Goals")

    # Get user input for goals
    goal = st.text_area("Enter your goal:")

    # Display goals
    st.write("Your Goals:")
    st.write(goal)

    # Save goal to data dictionary
    data["Goals"].append({"Goal": goal})

# Function to create social posts
def create_social_post():
    st.subheader("Create a Social Post")

    # Get user input for social post
    post_content = st.text_area("Enter post content:")

    # Display social post
    st.write("Your Social Post:")
    st.write(post_content)

    # Save social post to data dictionary
    data["Social Posts"].append({"Content": post_content})

# Function to display quote of the day
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

# Function to upload images
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

# Function to write data to CSV
def write_to_csv():
    df = pd.DataFrame.from_dict({(i,j): data[i][j] for i in data.keys() for j in range(len(data[i]))}, orient='index')
    df.to_csv("flashcards_data.csv", index_label=['Category', 'Index'])

# Function to view dashboard
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

# Heading and Paragraph text
st.title("Multifunctional App")

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
