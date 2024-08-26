import streamlit as st
import requests
import time
import ollama
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
# Custom CSS for cyberpunk theme
with open( "./css/main.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
phi3_client = ollama.Client(host='http://phi3:11434')

# Initialize session state for chat history
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if 'model' not in st.session_state:
        st.session_state['model'] = 'phi3:3.8b'
# Function to generate response based on selected AI model
def generate_response(prompt):
    response = ""
    response_placeholder = st.empty()
    for chunk in phi3_client.chat(model=st.session_state['model'], 
                              messages=[{'role': 'user', 'content': prompt}], 
                              stream=True,options={"temperature": 0.5, "top_k": 10, "min_p": 0.1}):
     
        response += chunk['message']['content']
        response_placeholder.markdown(response + "▌")
    response_placeholder.empty()
    return response

def onclick_callback():
    prompt = st.session_state.user_input
    with messages.chat_message("user", avatar="🤠"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with messages.chat_message(f"{st.session_state['model']}  - assistant", avatar="🤖"):
        with st.spinner("Processing..."):
            response = generate_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})

initialize_session_state()

# Sidebar for model selection & parameter input
st.sidebar.markdown("## Model Connection")
models = [model["name"] for model in phi3_client.list()["models"]]
# AI model selection
st.session_state['model'] = st.sidebar.selectbox("Select Model", models)
# TODO: Temperature, min P, and Top K sliders will go here
temp = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0,step=0.1, value=0.5)

st.title("Welcome to the AI Pod, Space Cowboy! 🌵")
st.markdown("## Models. Online.")
messages = st.container()
prompt_form = st.form("prompt-form",clear_on_submit=True)

       
# Display chat messages

for message in st.session_state.messages:
    if message["role"] == "user":
        avatar="🤠"
    else:
        avatar="🤖"
        
    with messages.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

with prompt_form:
    cols = st.columns((6,1),vertical_alignment="center")
    cols[0].text_input("Prompt", placeholder="Enter your prompt:", key="user_input",label_visibility="collapsed")
    cols[1].form_submit_button("🔄", type="primary", on_click=onclick_callback)



# Display a futuristic footer
st.markdown("---")
st.markdown("### CyberChat v2.0 | Powered by FreeTime")