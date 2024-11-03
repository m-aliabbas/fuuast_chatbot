# First we initialize the model we want to use.
from langchain_openai import ChatOpenAI
from agents.utils.topic_rag import  rag_response_generator
from langgraph.graph import StateGraph, END,MessagesState

import json
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool

from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(model="gpt-4o", temperature=0)
class MyState(MessagesState):
    pass


@tool
def get_fuuast_information(user_message):
    """This function/tool will provide information about the
     fedral urdu university of sart science and technology.
        If user ask about university it will reply.

        """
    result = rag_response_generator(user_message)
    return result


tools = [get_fuuast_information]

model = model.bind_tools(tools)

tools_by_name = {tool.name: tool for tool in tools}

# Define our tool node
def tool_node(state: MessagesState):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}

# Define the node that calls the model
def call_model(
    state: MyState,
    config: RunnableConfig,
):
    # this is similar to customizing the create_react_agent with state_modifier, but is a lot more flexible
    system_prompt = SystemMessage(
        "You are a helpful AI assistant at Fedral Urdu University of Arts Science and Technology Islamabad (FUUAST), please respond to the users query to the best of your ability!. Do not tell you are AI"
    )
    response = model.invoke([system_prompt] + state["messages"], config)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define the conditional edge that determines whether to continue or not
def should_continue(state: MyState):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"
    
from langgraph.graph import StateGraph, END

# Define a new graph
workflow = StateGraph(MyState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "tools",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("tools", "agent")
checkpointer = MemorySaver()
# Now we can compile and visualize our graph
compiled_graph = workflow.compile(checkpointer=checkpointer)


