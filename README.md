SQL Query Generator with LLM (Llama 3.1)
This project is a Streamlit-based web application that uses LangChain and Groq's Llama 3.1 model to generate SQL queries from natural language questions, run those queries on a connected SQL database, and convert the results back into a human-readable format. The application leverages LangChain for building SQL prompt templates and Groq's Chat API to interpret and respond to user queries.

Features
Natural Language to SQL: Converts plain English questions into SQL queries.
Automatic SQL Execution: Connects to an SQL database and runs the generated SQL query.
Readable Responses: Transforms SQL results into human-readable answers.
Chat Interface: Displays conversation history and interaction in a chat-based UI.
Prerequisites
Python 3.8+
Streamlit for the web interface
LangChain and LangChain-Community libraries
Groq API credentials for Chat model integration
MySQL database (or compatible SQL database) for query execution
File Overview
app.py: Main file for the Streamlit application.
README.md: Project documentation.
.env: Stores environment variables, like the Groq API key.
Code Breakdown
Database Initialization: init_database function connects to the SQL database.
Schema Retrieval: get_schema retrieves schema details from the database.
Prompt Generation: get_sql_chain creates a prompt for translating user questions into SQL.
LLM Query: get_llama_query_response sends the prompt to the LLM and retrieves the SQL query or response.
Human-Readable Responses: get_nl_response translates SQL results into natural language.
Example
User Query: "What are the top 10 highest-grossing movies in the database?"
LLM SQL Conversion: Generates an SQL query based on the database schema.
SQL Execution: The query runs, and results are fetched from the database.
Natural Language Response: The results are formatted as a human-readable answer.
