from typing import Literal
from langgraph.prebuilt.chat_agent_executor import AgentState
from typing_extensions import TypedDict


class Shirt(TypedDict):
    color: Literal["white", "black", "blue", "red", "green", "custom_colors"] = None
    size: Literal["xs", "s", "m", "l", "xl", "xxl"] = None
    gender: Literal["male", "female", "unisex"] = None
    printing_options: Literal["screen_printing", "embroidery",
                              "heat_transfer", "direct_to_garment"] = None
    style: Literal["crew_neck", "v-neck", "long_sleeve", "tank_top"] = None
