from streamlit import session_state as ss
import streamlit as st
import json
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredHTMLLoader
import shutil
from langchain_community.vectorstores import FAISS
#Checking if the database has been created and loaded. Used across files to ensure no queries are run without loading the database.
if "is_combined" not in st.session_state:
        st.session_state["is_combined"] = False
#Checking if the ticker has been selected. This session variable is used across files to ensure no queries are run without selecting a ticker first.
if "selected_ticker" not in st.session_state:
        st.session_state["selected_ticker"] = None

# Load the company mappings from a JSON file so that it's easy for the user to select a company from its name, rather than its ticker.
with open("D:\\ML\\FSIL\\ticker_dict.json", 'r') as file:
    company_mapping = json.load(file)

#Make a dictionary of company names and tickers
companies={}

for company in company_mapping.values():
    companies[company['title']]=company['ticker']


is_combined=False
def combine_files(ticker, year):
    consolidated_path = os.path.join('D:\ML\FSIL\sec-edgar-filings\\',ticker, "consolidated")
    primary_document_path = os.path.join("D:\ML\FSIL\sec-edgar-filings\\",ticker, "10-K",year, "primary-document.html")
    
    if not os.path.exists(consolidated_path):
        os.makedirs(consolidated_path)
    shutil.copy(primary_document_path, consolidated_path)
    os.chdir(consolidated_path)
    os.rename('primary-document.html',year+'.html')
    os.chdir("D:\\ML\\FSIL\\multipage")


st.title("FSIL Assignment: Bhuvan Koduru")
selected_company_name = st.selectbox("Select company name:", companies.keys(),index=1)
selected_ticker = companies[selected_company_name]
st.session_state["selected_ticker"] = selected_ticker
st.write("Selected ticker:", selected_ticker)
year_start = st.selectbox("Enter start year:", set(range(1995, 2024)))
year_end = st.selectbox("Enter end year:", set(range(year_start, 2024))) #Users shouldn't be able to select an end year less than the start year.

if st.button("Create and Load database"):
    with st.spinner('Making database...'):
        
        for year in range(year_start, year_end+1):
            combine_files(selected_ticker, str(year)[2:])
        loader=DirectoryLoader(f"D:\\ML\\FSIL\\sec-edgar-filings\\{selected_ticker}\\consolidated",loader_cls=UnstructuredHTMLLoader)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=1024)
        docs = text_splitter.split_documents(documents)
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.from_documents(docs, embedding_function)
        #Saving the FAISS db locally for easy access
        db.save_local(f"D:\\ML\\FSIL\\sec-edgar-filings\\{selected_ticker}\\consolidated\\db_add")

    is_combined=True
    st.session_state["is_combined"] = is_combined
    st.success('Database created and loaded!')