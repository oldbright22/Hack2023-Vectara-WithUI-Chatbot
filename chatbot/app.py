import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from chatbot import MaverickChatbot

st.set_page_config(page_title="Doctor Consultant", page_icon='💬')

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/4c/Hackathon-llm-2023.png")
    st.markdown('# 🤖 Menu ')
    st.markdown('''
    
    ### Purpose

    This AI is a helpful and casual consultation doctor named Kamal, whom it's purpose is designed to improve the patient consultation experience when research and discuss around subject of colorectal cancer.

    We believe this AI assisstant can help many patients worldwide.

    🏀🏓🏈🎳⚾🏒🥊⛳🤿🏏🎾🎿🏐⛸️🤖

    ###
    ''')

    st.markdown('💻 Source code on [Github] (https://github.com/oldbright22/Hack2023-Vectara-WithUI-Chatbot)')
    st.markdown('👨‍💻 Made by FutureTech Mavericks (https://tinyurl.com/Discord-MaverickTeam) ')
    
    
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["👨‍💻 Hello!"]

if 'past' not in st.session_state:
    st.session_state['past'] = ['']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()


def get_text():
    question = st.text_input("Your inquiry", "", key="input")
    return question


with input_container:
    st.markdown("💬 Welcome my name is Kamal, I'm an E-commerce assistant, how can I help you ?")
    user_input = get_text()


def generate_response(prompt):
    chatbot = MaverickChatbot()
    #db = chatbot.get_db_maverick()
    response = chatbot.get_response_from_query(prompt)

    #Here are some basic post-processing steps that can be applied to an AI model's outputs:
    response = response.replace("Mini ", "")
    response = response.replace("User ", "")
    response = response.replace("System.", "")
    response = response.replace("SYSTEM:", "")
    response = response.replace("Assistant ", "")


    prohibited_words = ["fuck", "shit"]
    for word in prohibited_words:
        response = response.replace(word, "****")

    response = response.strip()
    return response

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i), avatar_style="bottts-neutral", seed=90)
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style="avataaars-neutral", seed=10)


hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
