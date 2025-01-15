import streamlit as st
import pandas as pd
import pymongo
from io import StringIO
import base64
from pathlib import Path
from stringmatch import compute_similarity_score
import ast
from fuzzy import find_similar_texts_fuzzy
import numpy as np

if "output1" not in st.session_state:
    st.session_state.output1 = None
if "output2" not in st.session_state:
    st.session_state.output2 = None


# MongoDB Helper Function
def fetch_data_from_mongodb(uri, db_name, collection_name):
    client = pymongo.MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    data = pd.DataFrame(list(collection.find()))  # Converting MongoDB data to DataFrame
    return data

# File uploader function
def upload_excel_file(uploaded_file):
    return pd.read_excel(uploaded_file)

# Convert DataFrame to Excel for download
def to_excel(df):
    output = StringIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

# Function to generate a download link for the file
def download_link(df, filename="output.xlsx"):
    excel_file = to_excel(df)
    b64 = base64.b64encode(excel_file.getvalue().encode()).decode()  # encoding in base64
    return f'<a href="data:file/xlsx;base64,{b64}" download="{filename}"><button style="background-color: #FF5733; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold;">Download Excel File</button></a>'

# Streamlit App UI
def main():
    # Custom header with title and description
    st.markdown("""
    <style>
    .main-title {
        font-size: 45px;
        font-weight: bold;
        color: #FF5733;
        text-align: center;
        font-family: 'Arial', sans-serif;
        animation: fadeIn 2s ease-out;
    }
    .description {
        font-size: 18px;
        color: #888;
        text-align: center;
        font-family: 'Arial', sans-serif;
        animation: fadeIn 3s ease-out;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4CAF50, #388E3C);
        color: white;
        font-weight: bold;
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .sidebar-item {
        font-size: 18px;
        padding: 12px;
        cursor: pointer;
    }
    .sidebar .sidebar-item:hover {
        background-color: #66BB6A;
        border-radius: 5px;
        transition: 0.3s;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .container {
        background: linear-gradient(135deg, #f2f2f2, #ffffff);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .card {
        background: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

    def img_to_bytes(img_path):
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded

    def img_to_html(img_path):
        img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
            img_to_bytes(img_path)
        )
        return img_html

    st.markdown("<p style='text-align: right; color: white;'> " + img_to_html('kpmg.png') + "</p>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'> " + img_to_html('national_emblem_resized.png') + "</p>",
                unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: grey;'>KPMG DEMO</h3>", unsafe_allow_html=True)

    st.markdown('<p class="main-title">Nearest Search AI based Application</p>', unsafe_allow_html=True)
    st.markdown('<p class="description">Upload your data, fetch from MongoDB, or input raw text. Process and download as Excel.</p>', unsafe_allow_html=True)

    # Sidebar with enhanced styling
    st.sidebar.title("Data Input Methods")
    data_source = st.sidebar.radio(
        "Choose Data Source",
        ["Upload Excel File", "Fetch from MongoDB", "Input Raw Text"],
        help="Select the data source for your input"
    )

    # Create content layout with container
    if data_source == "Upload Excel File":
        # Excel Upload Section
        st.subheader("Upload Excel File")
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xls", "xlsx"])
        if uploaded_file:
            df = upload_excel_file(uploaded_file)
            st.dataframe(df, use_container_width=True)
            st.markdown(download_link(df), unsafe_allow_html=True)

    elif data_source == "Fetch from MongoDB":
        # MongoDB Section
        st.subheader("Fetch Data from MongoDB")
        uri = st.text_input("MongoDB URI (e.g., mongodb://localhost:27017)")
        db_name = st.text_input("Database Name")
        collection_name = st.text_input("Collection Name")

        if st.button("Fetch Data", use_container_width=True):
            if uri and db_name and collection_name:
                try:
                    df = fetch_data_from_mongodb(uri, db_name, collection_name)
                    if not df.empty:
                        st.dataframe(df, use_container_width=True)
                        st.markdown(download_link(df), unsafe_allow_html=True)
                    else:
                        st.error("No data found in the MongoDB collection.")
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
            else:
                st.error("Please provide valid MongoDB connection details.")

    elif data_source == "Input Raw Text":
        # Raw Text Section
        st.subheader("Input Raw Text data for comparision")

        raw_text_input = st.text_area("Enter Data input_text (list)", height=70)
        if raw_text_input:
            raw_text_compare = st.text_area("Enter compare_text (list of lists)", height=90)
            if raw_text_compare:
                input_text = ast.literal_eval(raw_text_input.strip())
                compare_text = ast.literal_eval(raw_text_compare.strip())
            if st.button('AI Based Score'):
                # When the button is clicked
                #st.write(f"input_text: {raw_text_input}, \n ,compare_text: {raw_text_compare}")
                try:
                    if type(input_text) == list:
                        if type(compare_text) == list:
                            if (len(compare_text)) > 0:
                                scores = compute_similarity_score(input_text, compare_text, metric="cosine")
                                transformer_score = {}
                                for match, score in scores.items():
                                    #st.write(f"{match}: {score}")
                                    transformer_score[match] = score
                                #st.session_state.output1 = f"AI based score: {transformer_score}"
                                st.session_state.output1 = transformer_score
                                #st.session_state.output1 = "AI based score"
                                # add fuzzy logic, call function
                                    # streamlit show button for fuzzy logic

                            else:
                                st.error("Got nothing to compare with, please provide compare_text list")
                        else:
                            st.error("Invalid Input Format, Recheck!!")
                    else:
                        st.error("Invalid Input Format, Recheck!!")


                except Exception as e:
                    st.error(f"Error fetching data: {e}")

            else:
                st.write("Waiting for submission...")
            if st.button('Fuzzy Score'):
                # When the button is clicked
                #st.write(f"input_text: {raw_text_input}, \n ,compare_text: {raw_text_compare}")
                try:
                    if type(input_text) == list:
                        if type(compare_text) == list:
                            if (len(compare_text)) > 0:
                                fuzzy_scores_list = find_similar_texts_fuzzy(input_text,compare_text)
                                fuzzy_score = {}

                                for index, value in enumerate(fuzzy_scores_list):
                                    calculated_score = str(value).split()[-1]
                                    clean_data = "".join(filter(lambda x: x.isdigit() or x == ".", calculated_score))  # Keeps only digits & dots
                                    num = float(clean_data)* .01
                                    fuzzy_score["Match with String "+str(index+1)]= num

                                st.session_state.output2 = fuzzy_score
                                #st.session_state.output2 = "Fuzzy score:"

                            else:
                                st.error("Got nothing to compare with, please provide compare_text list")
                        else:
                            st.error("Invalid Input Format, Recheck!!")
                    else:
                        st.error("Invalid Input Format, Recheck!!")


                except Exception as e:
                    st.error(f"Error fetching data: {e}")

            else:
                st.write("Waiting for submission...")

            # Display results side by side
            col1, col2 = st.columns(2)

            # First output (Always shown)
            with col1:
                st.subheader("AI based Score")
                st.write(st.session_state.output1)
                # for match, score in scores.items():
                #     st.write(f"{match}: {score}")
            # Second output (Only if Submit 2 was clicked)
            with col2:
                st.subheader("Fuzzy Score ")
                if st.session_state.output2:  # Show only if Submit 2 was clicked
                    st.write(st.session_state.output2)
                    # for index, value in enumerate(fuzzy_scores_list):
                    #     st.write(f"{str(value).split()[-1]}")
if __name__ == "__main__":
    main()
