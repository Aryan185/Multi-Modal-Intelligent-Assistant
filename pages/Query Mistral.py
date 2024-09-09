import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import Ollama
st.title("Mistral Bot")
if "is_combined" not in st.session_state:
        st.session_state["is_combined"] = False
if not st.session_state['is_combined']:
    st.warning("Please ensure the database has been created and loaded before querying")
else:
    if "messages_mistral" not in st.session_state:
        st.session_state.messages_mistral = []

# Display chat messages from history on app rerun
    for message in st.session_state.messages_mistral:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if user_query := st.chat_input("Enter your queries here"):
        # Display user message in chat message container
        st.chat_message("user").markdown(user_query)
        # Add user message to chat history
        st.session_state.messages_mistral.append({"role": "user", "content": user_query})
        with st.spinner('Generating answer...'):
    
            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            selected_ticker = st.session_state['selected_ticker']
            new_db = FAISS.load_local(f"D:\\ML\\FSIL\\sec-edgar-filings\\{selected_ticker}\\consolidated\\db_add", embedding_function,allow_dangerous_deserialization=True)
            docs_faiss = new_db.similarity_search(user_query)
            llm = Ollama(model='mistral')
            chain = load_qa_chain(llm, chain_type="stuff")
            answer = chain.run(input_documents=docs_faiss, question=user_query) 
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages_mistral.append({"role": "assistant", "content": answer})
