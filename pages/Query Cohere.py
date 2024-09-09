import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_core.prompts import ChatPromptTemplate
cohere="My API Key"
from langchain_cohere import ChatCohere
st.title("Cohere Bot")
if "is_combined" not in st.session_state:
        st.session_state["is_combined"] = False

if not st.session_state['is_combined']:
    st.warning("Please ensure the database has been created and loaded before querying")
else:
    if "messages_cohere" not in st.session_state:
        st.session_state.messages_cohere = []

# Display chat messages from history on app rerun
    for message in st.session_state.messages_cohere:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if user_query := st.chat_input("Enter your queries here"):
        # Display user message in chat message container
        st.chat_message("user").markdown(user_query)
        # Add user message to chat history
        st.session_state.messages_cohere.append({"role": "user", "content": user_query})
        with st.spinner('Generating answer...'):
    
            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            selected_ticker = st.session_state['selected_ticker']
            new_db = FAISS.load_local(f"D:\\ML\\FSIL\\sec-edgar-filings\\{selected_ticker}\\consolidated\\db_add", embedding_function,allow_dangerous_deserialization=True)
            docs_faiss = new_db.similarity_search(user_query)
            chat = ChatCohere(model="command",cohere_api_key=cohere)
            system = (
                "You are a helpful assistant that answers questions based on {context}. For every question asked, if you can find the answer within the context, generate beautiful visualisations such as pie charts and bar graphs. Be as analytical as possible. If you don't know the answer, just say that you don't know, don't try to make up an answer."

            )
            human = "{text}"
            prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

            chain = prompt | chat
            answer=chain.invoke(
                {
                    "context": docs_faiss[0].page_content,
                    "text": user_query,
                }
            )
            
        response = f"{answer.content}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages_cohere.append({"role": "assistant", "content": response})

