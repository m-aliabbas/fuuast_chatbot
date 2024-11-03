from agents.chat_agent import compiled_graph
from dotenv import load_dotenv


load_dotenv()

config = {"configurable": {"thread_id": "12122"}}
state= compiled_graph.invoke({'messages':['please tell me the address']},config=config)
print(state['messages'][-1].content)
