import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
from streamlit.logger import get_logger
from langchain_openai import ChatOpenAI
from utils import utils
from utils.streaming_handler import StreamHandler
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.prompt import PromptTemplate
from src.exam_agent import ChatBot
import pandas as pd
load_dotenv()
st.set_page_config(page_title="Fedral Urdu University of Arts Science and Technology Islamabad", page_icon="⭐")
st.header('Information Bot')
st.write('This is a Mockup UI for inital version')


class ContextChatbot:
    def __init__(self):
        utils.sync_st_session()
        if 'llm_chain' not in st.session_state:
            st.session_state.llm_chain = ChatBot()
        if 'thread_id' not in st.session_state:
            st.session_state.thread_id = str(datetime.now())
        

    def get_thread_id(self):
        return  st.session_state.thread_id
    def setup_chain(_self):
        return st.session_state.llm_chain
     
    @utils.enable_chat_history
    def chat_tab(self):
        # Tab 1 for chat interaction
        self.chain = self.setup_chain()
        self.thread_id = self.get_thread_id()
        user_query = st.chat_input(placeholder="Ask me anything!")
        utils.display_all_messages()
        if user_query:
            utils.display_msg(user_query, 'user')
            response = self.chain.chat(user_query,self.thread_id)
            utils.display_msg(response, 'assistant')

    def random_text_tab(self):
    # Tab 2 for random text or other 
        st.write("Developed by Faheem and team as FYP")
        st.write("V 1.0")

    def main(self):
        # Create two tabs
        tab1, tab2 = st.tabs(["Chat","About Developer"])

        # Chat functionality in tab1
        with tab1:
            self.chat_tab()

        with tab2:
            self.random_text_tab()
        # Random text or other content in tab2
        


if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()
