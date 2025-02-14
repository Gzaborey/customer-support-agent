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


# Initialize models
retriever = initialize_retriever()
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
    
    # Log the summary along with the timestamp
    log_file = os.path.join(LOGSDIR_PATH, "support_logs.txt")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] - {summary}\n")
    
    return "Support request logged successfully."

@tool
def get_faq_info(query: str) -> str:
    """
    Retrieve relevant documents from the Chroma vector store based on a query.
    """
    documents = retriever.invoke(query)
    faq_info = "\n".join([document.page_content for document in documents])
    return faq_info


@tool
def customize_order(attribute: str, value: str, state: Annotated[dict, InjectedState]) -> str:
    """
    Updates a T-shirt customization based on the provided customization request.
    Checks if there are remaining attributes to choose and guides the user accordingly.
    """
    
    if not is_valid_customization_attribute(attribute):
        available_options = ",".join(get_valid_shirt_attributes())
        return f"Sorry, we don't have such an option. Available options for customization are {available_options}."

    if not is_valid_customization_attribute_value(attribute, value):
        available_options = ",".join(get_valid_shirt_attribute_values(attribute))
        return f"Sorry, we don't have such an option. Available options for customizing the {attribute} are {available_options}."

    state["order"][attribute] = value

    remaining_attributes = [
        attr for attr in get_valid_shirt_attributes()
        if attr not in state["order"]
    ]

    if not remaining_attributes:
        shirt_specifications = ", ".join(f"{k}: {v}" for k, v in state["order"].items())
        return f"Customization is successful! The shirt customization is complete: {shirt_specifications}."

    next_attribute = random.choice(remaining_attributes)
    available_values = get_valid_shirt_attribute_values(next_attribute)
    return (
        f"Customization is successful! The {attribute} was set to {value}.\n"
        f"Please choose a value for {next_attribute}. Available options are: {available_values}."
    )