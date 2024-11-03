# Define the chat node
# def chat_node(state: MyState) -> MyState:
#     # Use ChatOpenAI to process the messages
#     # This is a placeholder for the actual ChatOpenAI logic
#     state['answers'].append(state['messages'][-1].content)
#     ai_message = llm.invoke(state['messages'][-1].content)
#     state["messages"].append(ai_message)
#     state["count"] = state.get("count",0) + 1
#     state['questions'].append(llm.invoke('Generate random General Knowlage Question')) 
#     return state

# # Define the summarize node
# def summarize_node(state: MyState) -> MyState:
#     # Use ChatOpenAI to summarize the messages
#     # This is a placeholder for the actual ChatOpenAI logic
#     state["messages"].append(AIMessage(content="Summary"))
#     return state

# def topic_generation_node(state: MyState) -> MyState:

#     state["messages"].append(AIMessage(content="Let talk on Maths"))
#     state['topic'] = 'math'
#     state["count"] = state.get("count",0) + 1 
#     return state

# graph.add_node("chat", chat_node)
# graph.add_node("summarize", summarize_node)
# graph.add_node("topic_generation", topic_generation_node)

# Add conditional edges
# def decide_next_node(state: MyState) -> str:
#     if len(state["messages"]) > 10:
#         return "summarize"
#     elif state["messages"] and isinstance(state["messages"][-1], AIMessage):
#         return END
    # else:
    #     return "chat"

# graph.add_conditional_edges(
#     "chat",
#     decide_next_node,
#     {"summarize": "summarize", END: END}
# )
