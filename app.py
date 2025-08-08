# app.py

# from chains.retrieval_qa import build_qa_chain

# qa_chain = build_qa_chain()

# while True:
#     query = input("\n You: ")
#     if query.lower() in ["exit", "quit"]:
#         break
#     result = qa_chain.invoke({"query": query})
#     answer = result["result"]
#     print(f"Bot: {answer}")


# from graph.conversation_graph import build_graph

# graph = build_graph()
# while True:
#     query = input("\n You: ")
#     if query.lower() in ["exit", "quit"]:
#         break
#     result = graph.invoke({"query": query})
#     answer = result["response"]
#     print(f"Bot: {answer}")


import streamlit as st
from langsmith_config import call_graph
from graph.conversation_graph import build_graph



st.set_page_config(page_title="Farming Chatbot")

st.title("Farming Chatbot")
st.caption("Type your message below to start the conversation.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    result = call_graph(prompt)
    response = result["response"]

    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
