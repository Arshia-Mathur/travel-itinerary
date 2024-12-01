import streamlit as st
import random
import time

st.title("Travel Dropbox BTT")
st.write("Input your content, and watch as our bot generates your travel itinerary and provides recommendations!")
st.caption("Note only PDFs, text, and images are permitted.")

# need to fix color
st.markdown("""
<style>
button {
    background-color: #456990;
    color: #D8E1EB;
}
</style>"""
, unsafe_allow_html=True)

with st.form("my_form"):
    st.write("Select one of the two modes of submitting.")
    
    # add dropdown menu so both don't show up at once 
    text_val = st.text_area("Copy and paste your email(s).",value="", placeholder="Emails", label_visibility="visible")
    
    uploaded_files = st.file_uploader(
    "Choose a file(s).", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("text", text_val, "image",uploaded_file )
st.text(" ")
# add on-click open the next form
# need to update button spacing
with st.form("itinerary_form"):
    st.write("Travel Itinerary")
    st.caption("Our generator compiles your content into an easy to read format. You may regenerate the itinerary as you see fit.")
    passengers = st.text_area("Passengers",value="", placeholder="Original response", label_visibility="visible")
    flights = st.text_area("Flight Information",value="", placeholder="Original response", label_visibility="visible")
    st.warning('Flight has already happened.', icon="⚠️")
    hotel = st.text_area("Hotel Information",value="", placeholder="Original response", label_visibility="visible")
    activities = st.text_area("Activities",value="", placeholder="Original response", label_visibility="visible")
    
    col1, col2 = st.columns(2)
    with col1:
        saved = st.form_submit_button("Save Itinerary")
    with col2:
        regenerated = st.form_submit_button("Regenerate Itinerary")
    # add actions for forms 

# will need to update edit vs safe versions 
with st.form("final_itinerary_form"):
    st.write("Travel Itinerary")
    st.caption("Safe travels!")
    with st.expander("Passengers"):
        st.write("1. Name: ")
    with st.expander("Flight Information"):
        st.write("Departure: ")
        st.write("Arrival: ")
        st.write("Booking Reference: ")
        st.write("Flight Code: ")
    with st.expander("Hotel Information"):
        st.write("Check-In: ")
        st.write("Check-Out: ")
        st.write("Address: ")
    with st.expander("Activities"):
        st.write("Title: ")
        st.write("Date: ")
        st.write("Reference: ")
    col1, col2 = st.columns(2)
    with col1:
        saved = st.form_submit_button("Export PDF")
    with col2:
        regenerated = st.form_submit_button("Save Text")
    # add on-click actions for forms 

# as something nice to have for project, can add these features at end once everything else is finalized 
st.text(" ")
st.subheader("Next Steps")

# space for a restaurant API, could be automatically called 

# placeholder code
def response_generator():
    yield "Placeholder, would be the list of recommendations"
        
# one option 
st.write("Restaurant Option 1")
with st.chat_message("assistant"):
    st.write("Would you now like restaurant recommendations?")

    prompt = st.chat_input("Say something")
    if prompt == "Yes":
        st.write(f"User wants restaurant recommendations based on itinerary information.") # existing location
        response = st.write_stream(response_generator())
    if prompt == "No":
        st.write("Have a good day!")
    #st.session_state.messages.append({"role": "assistant", "content": response})
       # end 
# other option, automatically done 
    # need to add call to API 
st.write("Restaurant Option 2")
with st.chat_message("assistant"):
    st.write("Based on your itinerary, we recommend these restaurants:")
    response = st.write_stream(response_generator())

# space for uber API
st.write("Uber")
with st.form("uber_call"):
    st.write("Space for Uber API")
    submitted = st.form_submit_button("Book Transportation")

# add back to top button


# PDF reader (pdf reader to text) 
import fitz # PyMuPDF
from pdf2image import convert_from_path
import pytesseract


def read_pdf(file):
    """Reads the uploaded PDF file and extracts its text."""
    text = ""
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return f"An error occurred while reading the uploaded file: {str(e)}"


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        # Extract text using PyMuPDF
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        doc.close()

        # Fallback to OCR if no text is found
        if not text.strip():
            images = convert_from_path(pdf_path)
            for img in images:
                text += pytesseract.image_to_string(img)
        return text

    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}"


# Streamlit File Uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Extract text from uploaded file
    st.subheader("Processing Uploaded File...")
    pdf_text = read_pdf(uploaded_file)
    
    # Display extracted text in Streamlit
    st.subheader("Extracted Text")
    st.text_area("PDF Text", pdf_text, height=300)

# Local File Processing (for standalone use)
pdf_path = "example.pdf"  # Replace with your local file path
try:
    extracted_text = extract_text_from_pdf(pdf_path)

    # Save extracted text to a file
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
    
    # Print completion message for local processing
    print("Extraction complete. Text saved to output.txt")

except Exception as e:
    print(f"Error processing local file: {str(e)}")

