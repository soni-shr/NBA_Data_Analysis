import streamlit as st
import pymssql
import pandas as pd
import base64
import re
from PIL import Image
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

server_name = 'latest-damg-7275-nba.database.windows.net'
database_name = 'nba'
username = 'nbaadmin'
password = 'Password@123'

# Define function to download the table as CSV
def download_csv(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv" style = "text-decoration: none;"><button style="background-color: #7c0d0e; color: #ffffff; border-radius: 12px; padding: 8px 16px; display: block; margin: 0 auto;text-decoration: none;">Download CSV file</button></a>'
    return href

# Define a connection function to Azure SQL Database

def connect_to_database(server, database, username, password):
    conn = pymssql.connect(server=server, database=database, user=username, password=password)
    return conn

# Define a function to retrieve table names from the database

def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    table_names = [row[0] for row in cursor]
    return table_names

# Define a function to retrieve data from the selected table

def get_table_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT TOP(1000) * FROM {table_name}")
    data = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    print(table_name)
    print(column_names)
    df = pd.DataFrame(data, columns=column_names)
    return df

def execute_sql_query(conn, query):

    if not re.match(r'^\s*SELECT\s+.*\s+FROM\s+', query, re.IGNORECASE):
        raise ValueError('Only SELECT queries are authorized')
    else:    
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            if cursor.description:
                column_names = [column[0] for column in cursor.description]
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=column_names)
                return df
            else:
                return None
        except Exception as e:
            return str(e)

def upload_to_azure(filecontent,file_name, container_name):
    connect_str = 'DefaultEndpointsProtocol=https;AccountName=bucketdamg7245;AccountKey=wnrBP0mZCCNV5lPZ5irP4tWrwcMyKTyIfFF/FfDrEOAsIec1uhkyQq6jv5KlDlObYW9yWDGprsTj+AStldGKoA==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob=file_name)
    blob_client.upload_blob(filecontent,overwrite=True)


# Define page 1
def page1():
    st.title('View Database Tables')
    
    # Create connection to database
    conn = connect_to_database(server_name, database_name, username, password)

    # Get the table names from the database
    table_names = get_table_names(conn)
    st.write('Select the table you want to view data for from the dropdown below')
    # Create a dropdown of table names
    selected_table = st.selectbox('Table name',table_names)

    # Retrieve the data from the selected table
    table_data = get_table_data(conn, selected_table)
    hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
    
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

    # Display the table
    st.dataframe(table_data, width=1000)

    st.write('Use the button below to download the csv of the Table above')
    # Provide an option to download the table as a CSV file
    st.markdown(download_csv(table_data), unsafe_allow_html=True)

# Define page 2
def page2():
    st.title('Player and Team Performance Dashboard')
    st.write('Interact and use our PowerBI Dashboard for Player and Team performance here')
    # Embed PowerBI report
    st.markdown("""<iframe title="Player Statistics - Player Statistics" width="1300" height="800" src="https://app.powerbi.com/reportEmbed?reportId=3eb21850-9017-41b1-8fb8-646fb8b85004&autoAuth=true&ctid=a8eec281-aaa3-4dae-ac9b-9a398b9215e7" frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

def page6():
    st.title('Player Physical Performance Dashboard')
    st.write('Interact and use our PowerBI Dashboard for Player Physical performance tracking here')
    # Embed PowerBI report
    st.markdown("""<iframe title="PlayerPerformanceStats - Page 1" width="1300" height="800" src="https://app.powerbi.com/reportEmbed?reportId=bd9eff09-0936-47f7-a5f5-4248aea12bdd&autoAuth=true&ctid=a8eec281-aaa3-4dae-ac9b-9a398b9215e7" frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

def page5():
    st.title('Playoffs Progression')
    st.write('Visualize the progression of your teams through each season playoffs here')
    # Embed PowerBI report
    st.markdown("""<iframe title="ulti_tree" width="1300" height="800" src="https://app.powerbi.com/reportEmbed?reportId=c9438bf9-df56-4e4a-a472-3087311ae7f6&autoAuth=true&ctid=a8eec281-aaa3-4dae-ac9b-9a398b9215e7" frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

    
def page3():
    hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
    st.title('Query Database')
    # Create connection to database
    conn = connect_to_database(server_name, database_name, username, password)
    query = st.text_area('Enter SQL Query', height=250)
    if st.button('Execute'):
        if not query:
            st.warning('Please enter a query')
        else:
            df_or_error = execute_sql_query(conn, query)
            if isinstance(df_or_error, pd.DataFrame):
                st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
                st.dataframe(df_or_error)
            else:
                st.error(df_or_error)

def page4():
    st.title('Upload CSV File to Azure Blob Storage')
    
    # Create a file uploader
    uploaded_file = st.file_uploader('Choose a CSV file',type=['csv'],accept_multiple_files=False)

    if uploaded_file is not None:
        # Save the file to a temporary directory
        print('filename:',uploaded_file.name)
        filename = uploaded_file.name
        filecontents = uploaded_file.getvalue()
        # Upload the file to Azure Blob storage
        container_name = 'nbadataset'
        upload_to_azure(filecontents, filename, container_name)
        st.write('Uploading file ',filename,'....')
        st.success('File uploaded successfully!')


# Create a sidebar with navigation
st.sidebar.image(Image.open("./nba.jpg"), width=225)
st.sidebar.title('Data Access Platform')
options = ['View Tables/Download Data', 'View Player and Team Performance','View Player Physical Performance','Visualize Playoffs Progression', 'Query Database', 'Upload Data']
selection = st.sidebar.radio('Go to', options)

# Show the appropriate page based on the user's selection
if selection == 'View Tables/Download Data':
    page1()
elif selection == 'View Player and Team Performance':
    page2()
elif selection == 'View Player Physical Performance':
    page6()
elif selection == 'Query Database':
    page3()
elif selection == 'Visualize Playoffs Progression':
    page5()
else:
    page4()