from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from app.utils import is_valid_customization_attribute, is_valid_customization_attribute_value, get_valid_shirt_attributes, get_valid_shirt_attribute_values
from typing import Annotated, Union
import random


def get_current_shirt_specifications(state: Annotated[dict, InjectedState]) -> str:
    return (
        f"Current shirt customization setup: "
        "".join(f"{attribute}: {value}" for attribute, value in state["order"].items())
        )

def validate_order_customization_input(attribute: str, value: str) -> Union[str, None]:
    if not is_valid_customization_attribute(attribute):
        available_options = ",".join(get_valid_shirt_attributes())
        return f"Sorry, we don't have such an option. Available options for customization are {available_options}."

    if not is_valid_customization_attribute_value(attribute, value):
        available_options = ",".join(get_valid_shirt_attribute_values(attribute))
        return f"Sorry, we don't have such an option. Available options for customizing the {attribute} are {available_options}."
    
@tool
def customize_order(attribute: str, value: str, state: Annotated[dict, InjectedState]) -> str:
    """
    Updates a T-shirt customization based on the provided customization request.
    Checks if there are remaining attributes to choose and guides the user accordingly.
    """
    attribute = attribute.lower()
    value = value.lower()
    
    if not is_valid_customization_attribute(attribute):
        available_options = ",".join(get_valid_shirt_attributes())
        return f"Sorry, we don't have such an option. Available options for customization are {available_options}."

    if not is_valid_customization_attribute_value(attribute, value):
        available_options = ",".join(get_valid_shirt_attribute_values(attribute))
        return f"Sorry, we don't have such an option. Available options for customizing the {attribute} are {available_options}."

    state["order"][attribute] = value

    remaining_attributes = [attribute for attribute, value in state["order"].items() if value is None]

    if not remaining_attributes:
        shirt_specifications = ", ".join(f"{attribute}: {value}" for attribute, value in state["order"].items())
        return (
            f"Customization is successful! The {attribute} was set to {value}.\n"
            f"The shirt customization is complete: {shirt_specifications}."
            )

    next_attribute = random.choice(remaining_attributes)
    available_values = get_valid_shirt_attribute_values(next_attribute)
    current_shirt_specifications = get_current_shirt_specifications(state)
    return (
        f"Customization is successful! The {attribute} was set to {value}.\n"
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



