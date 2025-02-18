from __future__ import annotations
from typing import Literal
from typing_extensions import TypedDict
from langgraph.prebuilt.chat_agent_executor import AgentState


class CustomerSupportAgentState(AgentState):
    order: Shirt
    id: str

class Shirt(TypedDict):
    color: Literal["white", "black", "blue", "red", "green", "custom_colors"]
    size: Literal["xs", "s", "m", "l", "xl", "xxl"]
    gender: Literal["male", "female", "unisex"]
    printing_options: Literal["screen_printing", "embroidery",
                              "heat_transfer", "direct_to_garment"]
    style: Literal["crew_neck", "v-neck", "long_sleeve", "tank_top"]
