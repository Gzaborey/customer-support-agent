import chainlit as cl
from langchain_core.messages import HumanMessage
from app.agent import Agent, create_agent_state

agent = Agent()

@cl.on_chat_start
async def on_chat_start():
    state = create_agent_state()
    cl.user_session.set("state", state)
    await cl.Message(content="Hi, I am the TeeCustomizer Ordering Assistant! Let's make your own customizable shirt! What color should it be?").send()

@cl.on_message
async def on_message(message: cl.Message):
    state = cl.user_session.get("state")
    
    state["messages"].append(HumanMessage(content=message.content))
    
    config = {"configurable": {"thread_id": state["id"]}}
    
    response = agent.agent.invoke({"messages": state["messages"],
                                   "order": state["order"],
                                   "id": state["id"]},
                                   config=config)
    
    cl.user_session.set("state", response)
    
    final_response = response["messages"][-1].content
    await cl.Message(content=final_response).send()
