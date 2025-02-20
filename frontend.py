import os
import json
import streamlit as st
import google.generativeai as genai
from PIL import Image
import pymongo
from pymongo.errors import BulkWriteError

# Function to initialize the Generative AI model
def init_genai_model(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config={"response_mime_type": "application/json"},
    )

# Function to process uploaded files and extract texts
def extract_text_from_images(uploaded_files, model):
    extracted_texts = []

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name, use_column_width=True)
        
        # Define prompt
        prompt = f'''
        Extract the text from the image. With the following json format:

        Desired JSON format:

        {{
        "img_name": "{uploaded_file.name}",
        "accountName": "DC ELECTRICAL & PROPERTY SERVICES LTD",
        "accountNumber": "10123919",
        "statementPeriod": "12 June to 30 June 2022",
        "paid_outTransactions": [
            {{
            "date": "15 Jun 22",
            "type": "VIS",
            "description": "GATWICK DROP OFF\nCRAWLEY",
            "amount": "-5.00"
            }}
        ],
        "openingBalance": "564.41",
        "closingBalance": "241.60",
        "paid_inTransactions": [
            {{
            "date": "15 Jun 22",
            "type": "BP",
            "description": "PRESTON J&S",
            "amount": "170.00"
            }}
        ]
        }}
        '''
        
        result = model.generate_content([prompt, image])
        extracted_texts.append(result.text)

    return extracted_texts

# Function to insert data into MongoDB
def insert_data_to_mongo(json_data, mongo_uri, db_name, collection_name):
    try:
        client = pymongo.MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        result = collection.insert_many(json_data)
        return len(result.inserted_ids)
    except BulkWriteError as e:
        return f"Bulk Write Error: {e.details}"
    except Exception as e:
        return f"Insertion Error: {str(e)}"

# Function to fetch all data from MongoDB
def fetch_data_from_mongo(mongo_uri, db_name, collection_name):
    try:
        client = pymongo.MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's default _id field
        return data
    except Exception as e:
        return f"Query Error: {str(e)}"

# Main function to execute the Streamlit app logic
def main():
    st.title("Bank Statement Aggregation")

    # Sidebar for API Key input
    st.sidebar.header("Settings")
    GOOGLE_API_KEY = st.sidebar.text_input("Enter Google API Key", type="password")
    MONGO_URI = st.sidebar.text_input("Enter MongoDB URI", value="mongodb://localhost:27017/")

    db_name = "financial_data"
    collection_name = "bank_statements"

    if GOOGLE_API_KEY:
        model = init_genai_model(GOOGLE_API_KEY)

    uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg", "gif", "bmp"], accept_multiple_files=True)

    if uploaded_files:
        extracted_texts = extract_text_from_images(uploaded_files, model)
        cleaned_data = [json.loads(item) if isinstance(item, str) else item for item in extracted_texts]
        
        current_directory = os.getcwd()
        output_file = os.path.join(current_directory, "extracted_texts.json")
        with open(output_file, "w") as f:
            json.dump(cleaned_data, f, indent=4)
        
        with open("extracted_texts.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        st.header("Extracted JSON Data")
        st.json(data)

    # MongoDB Insert Button
    if st.button("Insert Data into MongoDB"):
        if MONGO_URI:
            result = insert_data_to_mongo(data, MONGO_URI, db_name, collection_name)
            if isinstance(result, int):
                st.success(f"Inserted {result} documents into MongoDB.")
            else:
                st.error(result)
        else:
            st.error("MongoDB URI is required.")

    # MongoDB Query Button
    if st.button("Query Data from MongoDB"):
        if MONGO_URI:
            query_result = fetch_data_from_mongo(MONGO_URI, db_name, collection_name)
            if isinstance(query_result, list):
                st.header("Fetched Data from MongoDB")
                st.json(query_result)
            else:
                st.error(query_result)
        else:
            st.error("MongoDB URI is required.")

# Execute the main function
if __name__ == "__main__":
    main()
