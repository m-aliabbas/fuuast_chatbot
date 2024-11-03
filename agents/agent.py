# from langgraph.graph import StateGraph, MessagesState, END
# from langchain_core.messages import AIMessage, HumanMessage
# from langchain_openai import ChatOpenAI
# # Define the state with a messages key
# from typing import Annotated
# from typing_extensions import List
# from langgraph.graph.message import AnyMessage, add_messages
# from agents.utils.utils import *
# from agents.utils.nodes import *
# from dotenv import load_dotenv

# from langgraph.checkpoint.memory import MemorySaver
# from agents.utils.topic_rag import exam_prompt_generator

# load_dotenv()

# print(os.environ)
# llm = ChatOpenAI()

# class MyState(MessagesState):
#     pass




# def get_entry_point(state: MyState):
    
#     # first of all we need to check which type of message it is then we
#     # can specify which node to start 
#     # general_chat , start_exam, or next_question_node
#     messages_list = state['messages']
#     next_node = get_message_type(state["messages"][-1].content,state["messages"][:-1])

#     # we got the next node as start_exam 
#     if next_node == 'start_exam':
#         topic = state.get('topic',None)
#         if not topic or len(topic) < 2:
#             # we need to start the exam
#             return 'start_exam_node'
    
#     #  we got the next node as next_question_node
#     if next_node  == 'next_question_node':
#         # we need to get the next question
#         topic = state.get('topic',None)
#         if not topic or len(topic) < 2:
#             # we need to start the exam
#             return 'start_exam_node'
        
#         cur_question = state.get('cur_question',0)
#         if cur_question == len(state['questions']) - 1:
#             return 'evaluation_node'
        
#         return 'next_question_node'
    

#     return 'general_chat'

# # Create the graph
# graph = StateGraph(MyState)

# # Add nodes
# graph.add_node("general_chat", general_chat_node)
# graph.add_node("start_exam_node", start_exam_node)
# graph.add_node("next_question_node", next_question_node)
# graph.add_node("evaluation_node", evaluation_node)

# # Set entry point
# graph.set_conditional_entry_point(get_entry_point)

# # Add edge to END from summarize
# graph.add_edge("general_chat", END)
# graph.add_edge("start_exam_node", END)
# graph.add_edge("next_question_node", END)
# graph.add_edge('evaluation_node',END)

# # Compile the graph
# checkpointer = MemorySaver()

# compiled_graph = graph.compile(checkpointer=checkpointer)

# # config = {"configurable": {"thread_id": "12121"}}
# # state= compiled_graph.invoke({'messages':['lets stat exam']},config=config)
# # print(state['messages'][-1].content)
# # state= compiled_graph.invoke({'messages':['i dont know lets ask next']},config=config)
# # print(state['messages'][-1].content)