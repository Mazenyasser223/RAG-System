import streamlit as st
from graph import app

st.title("🚀 Tech Giants Strategic Assistant")
st.markdown("Ask anything about the top 10 tech companies.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = app.invoke({"question": prompt})
            response = result["generation"]
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})