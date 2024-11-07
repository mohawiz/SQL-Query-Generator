# Import necessary libraries
import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from langchain_groq.chat_models import ChatGroq
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage

# Load environment variables
load_dotenv()

# Configure Groq API for Llama 3.1 model
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model_name="llama-3.1-70b-versatile", api_key=GROQ_API_KEY)

# Function to initialize SQL database connection
def init_database(db_user: str, db_password: str, db_host: str, db_name: str) -> SQLDatabase:
    return SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# Retrieve schema information
def get_schema(db):
    return db.get_table_info()

# Create SQL prompt template
def get_sql_chain(schema, chat_history, question):
    template = """
    You are an expert in converting English questions to SQL query!
    Based on the schema below, write an SQL query to answer the user's question.
    <SCHEMA>{schema}</SCHEMA>
    Conversation History: {chat_history}
    Question: {question}
    SQL Query:
    """
    return template.format(schema=schema, chat_history=chat_history, question=question)

# Convert SQL result to natural language response
def get_nl_response(sql_query, schema, sql_response):
    template = """
    Based on the schema and SQL response, translate the SQL result into a human-readable response.
    <SCHEMA>{schema}</SCHEMA>
    Sql_execution_response: {sql_response}
    SQL query: {sql_query}
    Response:
    """
    return template.format(sql_query=sql_query, schema=schema, sql_response=sql_response)

# Groq API call functions using Llama 3.1
def get_llama_query_response(prompt):
    try:
        response = llm.chat(prompt)
        return response.content.strip()  # Return the content from the LLM response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit app
st.set_page_config(page_title="SQL Query Generator with LLM")
st.header("Query Your Database")

# Sidebar for database connection
with st.sidebar:
    st.subheader("Database Connection")
    host = st.text_input("Host", value="localhost", key="host")
    user = st.text_input("User", key="user")
    password = st.text_input("Password", type="password", key="password")
    database = st.text_input("Database", key="database")

    if st.button("Connect"):
        with st.spinner("Connecting to the database..."):
            db = init_database(user, password, host, database)
            st.session_state["db"] = db
            st.success("Connected to the database!")

# Display chat history
for message in st.session_state.get("chat_history", []):
    with st.chat_message("ai" if isinstance(message, AIMessage) else "human"):
        st.markdown(message.content)

# Retrieve schema and interact with LLM if connected
if "db" in st.session_state:
    schema = get_schema(st.session_state["db"])

user_query = st.chat_input("Type a message...")
if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("human"):
        st.markdown(user_query)
        
    # Process query to SQL
    prompt = get_sql_chain(schema, st.session_state["chat_history"], user_query)
    sql_query = get_llama_query_response(prompt)
    
    # Execute SQL query and convert to natural language
    if sql_query:
        sql_response = st.session_state["db"].run(sql_query)
        response_prompt = get_nl_response(sql_query, schema, sql_response)
        response = get_llama_query_response(response_prompt)
        with st.chat_message("ai"):
            st.markdown(response)
        
        # Add response to chat history
        st.session_state.chat_history.append(AIMessage(content=response))
