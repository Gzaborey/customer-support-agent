import chainlit as cl
from langchain_core.messages import HumanMessage
from app.agent import Agent

agent_instance = Agent()

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("state", {"messages": [], "order": {}})
    await cl.Message(content="Hi, I am the TeeCustomizer Ordering Assistant! Let's make your own customizable shirt! What color should it be?").send()

@cl.on_message
async def on_message(message: cl.Message):
    state = cl.user_session.get("state", {"messages": [], "order": {}})
    
    state["messages"].append(HumanMessage(content=message.content))
    
    config = {"configurable": {"thread_id": cl.context.session.id}}
    
    response = agent_instance.agent.invoke({"messages": state["messages"], "order": state["order"]}, config=config)
    
    cl.user_session.set("state", response)
    
    final_response = response["messages"][-1].content
    await cl.Message(content=final_response).send()
