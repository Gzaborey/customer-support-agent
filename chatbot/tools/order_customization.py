from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from chatbot.utils import (is_valid_customization_attribute, is_valid_customization_attribute_value,
                       get_valid_shirt_attributes, get_valid_shirt_attribute_values,
                       get_current_shirt_specifications)
from typing import Annotated
import random

    
@tool
def customize_order(input_attribute: str, input_value: str, state: Annotated[dict, InjectedState]) -> str:
    """
    Updates a T-shirt customization based on the provided customization request.
    Checks if there are remaining attributes to choose and guides the user accordingly.
    """
    input_attribute = input_attribute.lower()
    input_value = input_value.lower()
    
    if not is_valid_customization_attribute(input_attribute):
        available_options = ",".join(get_valid_shirt_attributes())
        return (
            "Sorry, we don't have such an option." 
            f"Available options for customization are {available_options}."
            )

    if not is_valid_customization_attribute_value(input_attribute, input_value):
        available_options = ",".join(get_valid_shirt_attribute_values(input_attribute))
        return (
            "Sorry, we don't have such an option."
            f"Available options for customizing the {input_attribute} are {available_options}."
        )

    state["order"][input_attribute] = input_value

    remaining_attributes = [attribute for attribute, value in state["order"].items() if value is None]

    if not remaining_attributes:
        shirt_specifications = ", ".join(f"{attribute}: {value}" for attribute, value in state["order"].items())
        return (
            f"Customization is successful! The {input_attribute} was set to {input_value}.\n"
            f"The shirt customization is complete: {shirt_specifications}."
            )

    next_attribute = random.choice(remaining_attributes)

    available_values = get_valid_shirt_attribute_values(next_attribute)
    current_shirt_specifications = get_current_shirt_specifications(state)
    return (
        f"Customization is successful! The {input_attribute} was set to {input_value}.\n"
        f"Please choose a value for {next_attribute}. Available options are: {available_values}.\n"
        f"{current_shirt_specifications}"
        )

@tool
def check_order_status(state: Annotated[dict, InjectedState]) -> str:
    """
    Checks the status of the shirt customization order.

    Returns: 
    A string with the current status of the user's order.
    """
    return get_current_shirt_specifications(state)

# @tool
# def confirm_order(state: Annotated[dict, InjectedState]) -> str:
#     pass



