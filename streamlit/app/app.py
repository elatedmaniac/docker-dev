import streamlit as st
import requests
import time
import ollama
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
#import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
# Custom CSS for cyberpunk theme

import base64

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(img):
    bin_str = get_base64_of_bin_file(img)
    page_bg_img = '''
    <style>
    .stApp {
        background-size: cover;
        background-color: rgba(0, 0, 0, 0.6);
        background-blend-mode: overlay;
        background-image: url("data:image/png;base64,%s");
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
phi3_client = ollama.Client(host='http://phi3:11434')

# Initialize session state for chat history
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if 'model' not in st.session_state:
        st.session_state['model'] = 'phi3:3.8b'
    if 'temp' not in st.session_state:
        st.session_state['temp'] = 0.1
    if 'topk' not in st.session_state:
        st.session_state['topk'] = 10
    if 'minP' not in st.session_state:
        st.session_state['minP'] = 0.1   
# Function to generate response based on selected AI model
def generate_response(prompt):
    response = ""
    response_placeholder = st.empty()
    for chunk in phi3_client.chat(model=st.session_state['model'], 
                              messages=[{'role': 'user', 'content': prompt}], 
                              stream=True,options={"temperature": st.session_state['temp'], 
                                                   "top_k": st.session_state['topk'], 
                                                   "min_p": st.session_state['minP']}):
     
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
            st.markdown(f"Temp: {st.session_state['temp']}\tTop K: {st.session_state['topk']}\tMin. P: {st.session_state['minP']}")
            st.session_state.messages.append({"role": "assistant", "content": response})

def set_custom_slider_styles():
    slider_styles = """
    <style>
    /* Change the color of the slider track */
    .stSlider > div > div > div > div {
        background-color: #ffffff !important;
    }

    
    /* Change the color of the slider label */
    .stSlider > div > div > div > div > div > div {
        color: #ffffff !important;
    }
    </style>
    """
    st.markdown(slider_styles, unsafe_allow_html=True)

# Call this function before creating the sliders
set_custom_slider_styles()

with open("css/main.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
initialize_session_state()
set_png_as_page_bg('img/city.jpg')
# Sidebar for model selection & parameter input
with st.sidebar:
    st.markdown("## Model Connection")
    models = [model["name"] for model in phi3_client.list()["models"]]
    # AI model selection
    st.session_state['model'] = st.sidebar.selectbox("Select Model", models)

    st.session_state['temp'] = st.slider("Temperature", min_value=0.0, max_value=1.0,step=0.1, value=0.5)
    
    st.session_state['minP'] = st.slider("Min. P", min_value=0.0, max_value=1.0,step=0.1, value=0.1)
    
    st.session_state['topk'] = st.slider("Top K", min_value=0, max_value=250,step=2, value=10)
    
   
with st.container():
  
    st.markdown("## Welcome to the AI Pod!")
    
    
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
st.markdown("## Powered by FreeTime")