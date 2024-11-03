from agents.chat_agent import compiled_graph
from dotenv import load_dotenv
import json
class ChatBot:
    def __init__(self):
        self.chain = compiled_graph
        self.state = {}

    def  chat(self, message,thread_id):
        config = {"configurable": {"thread_id": thread_id}}
        response = self.chain.invoke({'messages': [message]},config=config)
        self.state = response
        # print(self.state)
        return response['messages'][-1].content
    
    def get_evaluation_results(self):
        pass

    