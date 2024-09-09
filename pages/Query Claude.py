import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
st.title("Claude Bot")
if "is_combined" not in st.session_state:
        st.session_state["is_combined"] = False
if not st.session_state['is_combined']:
    st.warning("Please ensure the database has been created and loaded before querying")
else:
    if "messages_claude" not in st.session_state:
        st.session_state.messages_claude = []

# Display chat messages from history on app rerun
    for message in st.session_state.messages_claude:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if user_query := st.chat_input("Enter your queries here"):
        # Display user message in chat message container
        st.chat_message("user").markdown(user_query)
        # Add user message to chat history
        st.session_state.messages_claude.append({"role": "user", "content": user_query})
        with st.spinner('Generating answer...'):
            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            selected_ticker = st.session_state['selected_ticker']
            new_db = FAISS.load_local(f"D:\\ML\\FSIL\\sec-edgar-filings\\{selected_ticker}\\consolidated\\db_add", embedding_function,allow_dangerous_deserialization=True)
            docs_faiss = new_db.similarity_search(user_query)
            context = ''
            for item in docs_faiss:
                context = context + "\n" + item.page_content
            
            chat = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229",anthropic_api_key='My API Key')

            system = ("You are a helpful assistant that answers questions based on {context}. For every question asked, if you can find the answer within the context, generate beautiful visualisations such as pie charts, bar graphs and other types of graphs using online tools that can be used to view them. Ensure the link to the chart is on a new line"
            )
            human = "{text}"
            prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

            chain = prompt | chat
            answer=chain.invoke(
                {
                    "context": context,
                    "text": user_query
                }
            )
        with st.chat_message("assistant"):
            st.markdown(answer.content)
        # Add assistant response to chat history
        st.session_state.messages_claude.append({"role": "assistant", "content": answer.content})

