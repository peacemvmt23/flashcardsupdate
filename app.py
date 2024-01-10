import streamlit as st

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

# Function to customize flashcards
def customize_flashcards():
    st.subheader("Customize Flashcards")

    # Get user input for customization
    font_color = st.color_picker("Choose font color:")
    background_color = st.color_picker("Choose background color:")

    # Display customized flashcard
    st.write("Customized Flashcard:")
    st.markdown(
        f'<div style="color:{font_color}; background-color:{background_color}; padding:10px;">'
        f'Customized Flashcard Content'
        f'</div>',
        unsafe_allow_html=True,
    )

# Function to view flashcard library
def view_flashcard_library():
    st.subheader("Flashcard Library")

    # Display flashcard templates
    st.write("Flashcard Templates:")
    st.write("1. Template 1")
    st.write("2. Template 2")
    # Add more templates as needed

# Heading and Paragraph text
st.title("Flashcards App")
st.markdown(
    "Welcome to the Flashcards App! Create engaging and informative flashcards "
    "with text, images, and web-links. Customize the fonts, colors, and text to go "
    "with your brand."
)

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select a page",
    ["Create Flashcard", "Customize Flashcards", "Flashcard Library"]
)

# Main content based on user selection
if page == "Create Flashcard":
    create_flashcard()
elif page == "Customize Flashcards":
    customize_flashcards()
elif page == "Flashcard Library":
    view_flashcard_library()
