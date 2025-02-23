from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from typing import Annotated
import os
from langchain_openai import ChatOpenAI
from chatbot.prompts import summarizer_prompt
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from chatbot.config import LOGSDIR_PATH
from datetime import datetime


summarizer = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@tool
def log_support_request(state: Annotated[dict, InjectedState]) -> str:
    """
    Use this tool if a customer needs to leave a message to support team.
    Extract key details from the user request and log them. 
    """
    # Extract message history
    message_history = state["messages"]

    # Trim the message history
    if len(message_history) > 10:
        message_history = message_history[-10:]
    else:
        message_history = message_history

    # Leave only Human and AI messages with their message content
    filtered_message_history = []

    for message in message_history:
        if isinstance(message, HumanMessage):
            filtered_message_history.append(HumanMessage(content=message.content))
        elif isinstance(message, AIMessage):
            filtered_message_history.append(AIMessage(content=message.content))
    
    summarizer_input = [SystemMessage(content=summarizer_prompt)] + filtered_message_history
    response = summarizer.invoke(summarizer_input)

    user_id = state["id"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = response.content if hasattr(response, "content") else "No summary produced."

    log_file = os.path.join(LOGSDIR_PATH, "support_logs.txt")
    with open(log_file, "a") as f:
        f.write(f"{user_id} - [{timestamp}] - {summary}\n")
    
    return "Support request logged successfully."
