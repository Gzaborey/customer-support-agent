from dotenv import load_dotenv
import os
import chromadb
from chatbot.prompts import system_prompt, initial_agent_message
from langchain_core.messages import AIMessage, SystemMessage
from langgraph.prebuilt import InjectedState
from typing import get_type_hints, get_args
from chatbot.config import CHROMADB_PATH
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from chatbot.schemas import Shirt, CustomerSupportAgentState
from uuid import uuid4
from typing import Union, List, Annotated

    
def get_valid_shirt_attributes() -> list[str]:
    return list(get_type_hints(Shirt).keys())

def get_valid_shirt_attribute_values(attribute: str) -> list[str]:
    try:
        return list(get_args(get_type_hints(Shirt)[attribute]))
    except ValueError as e:
        raise ValueError(f"The attribute is invalid. Error: {e}")

def is_valid_customization_attribute(attribute: str) -> bool:
    return attribute in get_valid_shirt_attributes()

def is_valid_customization_attribute_value(attribute: str, value: str) -> bool:
    return value in get_valid_shirt_attribute_values(attribute)

def get_current_shirt_specifications(state: Annotated[dict, InjectedState]) -> str:
    return (
        f"Current shirt customization setup: "
        "".join(f"{attribute}: {value}" for attribute, value in state["order"].items())
        )

def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key

def initialize_huggingface_retriever(
        embedding_model="BAAI/llm-embedder",
        chromadb_path=CHROMADB_PATH,
        collection_name="faq_collection"
        ) -> HuggingFaceEmbeddings:
    embedding_function = HuggingFaceEmbeddings(model_name=embedding_model)

    persistent_client = chromadb.PersistentClient(path=chromadb_path)

    vector_store = Chroma(
    client=persistent_client,
    collection_name=collection_name,
    embedding_function=embedding_function,
    create_collection_if_not_exists=False
    )
    
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6},
        lambda_mult=0
        )
    return retriever

def create_new_shirt() -> Shirt:
    return {attribute: None for attribute in get_valid_shirt_attributes()}

def create_user_id() -> str:
    return str(uuid4())

def create_initial_message_history(
        system_prompt: str = system_prompt,
        initial_agent_message: str = initial_agent_message
        ) -> List[Union[SystemMessage, AIMessage]]:
    new_message_history = [SystemMessage(content=system_prompt),
                           AIMessage(content=initial_agent_message)]
    return new_message_history

def create_new_agent_state() -> CustomerSupportAgentState:
    state = CustomerSupportAgentState()

    state["messages"] = create_initial_message_history(
        system_prompt=system_prompt,
        initial_agent_message=initial_agent_message
        )
    state["order"] = create_new_shirt()
    state["id"] = create_user_id()
    return state

def create_agent_config(state: CustomerSupportAgentState) -> dict:
    try:
        return {"configurable": {"thread_id": state["id"]}}
    except KeyError:
        raise RuntimeError("Input does not have 'id' field." 
                           "Input is not a valid agent state.")