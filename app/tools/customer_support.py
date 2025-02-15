from app.common.utils import initialize_retriever
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from app.common.utils import is_valid_customization_attribute, is_valid_customization_attribute_value, get_valid_shirt_attributes, get_valid_shirt_attribute_values
from typing import Annotated
import random
import os
from langchain_openai import ChatOpenAI
from app.prompts import summarizer_prompt
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import LOGSDIR_PATH
from datetime import datetime


summarizer = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@tool
def log_support_request(user_request: str) -> str:
    """
    Extract key details from the user request and log them.
    """
    summarization_input = [SystemMessage(content=summarizer_prompt), HumanMessage(content=user_request)]

    response = summarizer.invoke(summarization_input)
    summary = response.content if hasattr(response, "content") else "No summary produced."

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_file = os.path.join(LOGSDIR_PATH, "support_logs.txt")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] - {summary}\n")
    
    return "Support request logged successfully."