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
    relevant_messages = [message.content for message in state["messages"][:-5] 
                         if isinstance(message, HumanMessage) or isinstance(message, AIMessage)]

    # Leave only 4 last messages
    if len(relevant_messages) < 4:
        chosen_messages = relevant_messages
    else:

        chosen_messages = relevant_messages[-4:]
    summarization_input = [SystemMessage(content=summarizer_prompt)] + chosen_messages

    response = summarizer.invoke(summarization_input)

    user_id = state["id"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = response.content if hasattr(response, "content") else "No summary produced."

    log_file = os.path.join(LOGSDIR_PATH, "support_logs.txt")
    with open(log_file, "a") as f:
        f.write(f"{user_id} - [{timestamp}] - {summary}\n")
    
    return "Support request logged successfully."
