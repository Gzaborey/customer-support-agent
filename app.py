import chainlit as cl
from langchain_core.messages import HumanMessage
from chatbot.agent import CustomerSupportAgent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from chatbot.tools.customer_support import log_support_request
from chatbot.tools.faq import get_faq_info
from chatbot.tools.order_customization import customize_order, check_order_status
from chatbot.utils import create_new_agent_state, create_agent_config, load_api_key
from chatbot.prompts import initial_agent_message

# Agent initialization
api_key = load_api_key()

model = ChatOpenAI(name="gpt-4o-mini", temperature=0, api_key=api_key)
tools = [log_support_request, get_faq_info, customize_order, check_order_status]
memory = MemorySaver()

agent = CustomerSupportAgent(model=model, tools=tools, memory=memory)
agent.compile_agent()


@cl.on_chat_start
async def on_chat_start():
    state = create_new_agent_state()
    config = create_agent_config(state)

    cl.user_session.set("state", state)
    cl.user_session.set("config", config)

    await cl.Message(content=initial_agent_message).send()

@cl.on_message
async def on_message(message: cl.Message):
    state = cl.user_session.get("state")
    config = cl.user_session.get("config")
    
    state["messages"].append(HumanMessage(content=message.content))
    
    response = agent.run(state, config=config)
    
    cl.user_session.set("state", response)
    
    final_response = response["messages"][-1].content
    await cl.Message(content=final_response).send()
