# Streamlit Bank Statement Aggregation App

## Overview

This Streamlit application extracts text from uploaded bank statement images using Google Gemini AI and allows storing/querying the extracted data in a MongoDB database.

## Prerequisites

Ensure you have the following installed and set up:

-   **MongoDB** or **MongoDB Compass** for database management.
-   **Python 3.8+** installed on your system.
-   **Google Gemini API Key** to process image text extraction.

## Installation

1.  **Clone the repository**:
    
    ```sh
    git clone https://github.com/Mohsin-Ali-Mirza/bank_statement_gemini
    cd your-repository
    
    ```
    
2.  **Install dependencies**:
    
    ```sh
    pip install -r requirements.txt
    
    ```
    

## Running the Application

1.  **Start the Streamlit app**:
    
    ```sh
    streamlit run frontend.py
    
    ```
    
2.  **Enter your Google Gemini API key**:
    
    -   On the sidebar, enter your API key (you can create one [here](https://aistudio.google.com/apikey)) and press Enter.

3.  **Upload one or multiple bank statement images**:
    
    -   The application will extract text and display it in JSON format.
4.  **Insert extracted data into MongoDB**:
    
    -   Click the "Insert Data into MongoDB" button to store the extracted data.
5.  **Query stored data from MongoDB**:
    
    -   Click the "Query Data from MongoDB" button to retrieve and display stored data.

## Configuration

-   Modify `MONGO_URI` in the application to connect to your specific MongoDB instance.
-   Adjust JSON parsing if your bank statements have a different format.
