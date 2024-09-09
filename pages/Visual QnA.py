import streamlit as st
st.title("Visual QnA using LlaVa")
import ollama
image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
if image is not None:
    query = st.text_input("Enter your query")
if st.button("Submit Query"):
    file=image.getvalue()
    with st.spinner('Generating answer...'):
        response = ollama.chat(
            model='llava',
            messages=[
            {
                'role': 'user',
                'content': query,
                'images': [file],
            },
            ],
        )
    print(response['message']['content'])
    st.write(response['message']['content'])