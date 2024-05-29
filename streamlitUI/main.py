import streamlit as st
import pandas as pd
import json
import ast

st.set_page_config(page_title="watsonx.ai", page_icon="world ", layout="wide", initial_sidebar_state="expanded")

@st.cache_resource
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

data_file_path = "<insert csv file>"  # Update with your new CSV file path
data = load_data(data_file_path)

logo_image = "<insert path to logo>"  # Update with your logo file path
st.image(logo_image, use_column_width=False, width=300)

# Initialize session state variables if they don't exist
if 'selected_conversation_id' not in st.session_state:
    st.session_state['selected_conversation_id'] = None
    st.session_state['selected_data_date'] = None

def update_conversation_state(conversation_id, data_date):
    st.session_state['selected_conversation_id'] = conversation_id
    st.session_state['selected_data_date'] = data_date

# Sidebar search logic
def search_sidebar():
    st.sidebar.header("Search by ID, Date, or Client ID")
    search_query = st.sidebar.text_input("Enter Conversation ID, Date, or Client ID", placeholder="Enter Conversation ID, Date, or Client ID to search")
    return search_query

search_query = search_sidebar()

# Filter function based on search query
def filter_conversations(query):
    if query:
        return data[(data['conversationid'].str.contains(query, na=False)) | 
                    (data['data_date'].str.contains(query, na=False)) |
                    (data['derived_clientid'].astype(str).str.contains(query, na=False))]
    return data

filtered_conversations = filter_conversations(search_query)

# Function to create an accordion for each client
def create_client_accordions(filtered_conversations):
    grouped = filtered_conversations.groupby('derived_clientid')
    for client_id, group in grouped:
        with st.sidebar.expander(f"Client ID: {client_id}", expanded=True):
            for conversation_id, date in group[['conversationid', 'data_date']].values:
                if st.button(f"ID: {conversation_id} | Date: {date}", key=f"btn_{conversation_id}_{date}"):
                    update_conversation_state(conversation_id, date)

create_client_accordions(filtered_conversations)

st.title("Conversation Details")
left_column, right_column = st.columns(2)

# Right column for editable Transcript
with right_column:
    if st.session_state['selected_conversation_id']:
        filtered_data = data[
            (data["conversationid"] == st.session_state['selected_conversation_id']) &
            (data["data_date"] == st.session_state['selected_data_date'])
        ]

        if not filtered_data.empty:
            selected_transcript = filtered_data["transcript"].iloc[0]
            
            toggle_button = st.checkbox("Speaker Transcript")
            if toggle_button:
                selected_transcript = filtered_data["speaker_transcript"].iloc[0]

            st.text_area("Transcript", selected_transcript, height=695)

# Left column for other details
with left_column:
    if st.session_state['selected_conversation_id']:
        st.write("Selected Conversation ID:", st.session_state['selected_conversation_id'])

        if not filtered_data.empty:
            with st.expander("Summary of the Call", expanded=True):
                selected_summary = filtered_data["summary_combined"].iloc[0]
                edited_summary = st.text_area("summary", selected_summary, height=150,label_visibility="hidden")
            
            with st.expander("Category of the Call", expanded=True):
                selected_categories = filtered_data["categories"].iloc[0]
                st.text_area("categories", selected_categories, height=10,label_visibility="hidden")

            with st.expander("Recommended Next Steps/Action Items", expanded=True):
                selected_next_steps = filtered_data["next_steps_mixtral2"].iloc[0]
                st.text_area("next steps", selected_next_steps, height=300,label_visibility="hidden")

            with st.expander("Account Holdings Identified", expanded=True):
                selected_holdings = filtered_data["holdings"].iloc[0]
                st.text_area("holdings", selected_holdings, height=250,label_visibility="hidden")

            with st.expander("Products/Accounts Mentioned", expanded=False):
                selected_products = filtered_data["products_mixtral"].iloc[0]
                st.text_area("products", selected_products, height=250,label_visibility="hidden")
            
            with st.expander("Client Relationships Identified", expanded=False):
                selected_client_relationships = filtered_data["client_relationships_mixtral"].iloc[0]
                st.text_area("relations", selected_client_relationships, height=100,label_visibility="hidden")

            with st.expander("Purpose of the Call", expanded=False):
                selected_purpose = filtered_data["purpose_mixtral"].iloc[0]
                st.text_area("purpose", selected_purpose, height=250,label_visibility="hidden")

            with st.expander("Sentiment Analysis", expanded=False):
                selected_categories = filtered_data["sentiment"].iloc[0]
                st.text_area("overall sentiment", selected_categories, height=30,label_visibility="hidden")
            
            with st.expander("Risk Tolerance Identified", expanded=False):
                selected_risks = filtered_data["risks_mixtral"].iloc[0]
                st.text_area("risk", selected_risks, height=250,label_visibility="hidden")
            
            with st.expander("Entities", expanded=True):
                selected_categories = filtered_data["entities"].iloc[0]
                st.text_area("entities", selected_categories, height=300,label_visibility="hidden")


# Ensure this part is outside of the columns
if not st.session_state['selected_conversation_id']:
    st.warning("No conversation selected. Please choose a conversation.")
