from typing import Literal, Optional
from typing_extensions import TypedDict


class Shirt(TypedDict):
    color: Literal["white", "black", "blue", "red", "green", "custom_colors"]
    size: Literal["xs", "s", "m", "l", "xl", "xxl"]
    gender: Literal["male", "female", "unisex"]
    printing_options: Literal["screen_printing", "embroidery",
                              "heat_transfer", "direct_to_garment"]
    style: Literal["crew_neck", "v-neck", "long_sleeve", "tank_top"]

class Customer(TypedDict):
    name: Optional[str]
    surname: Optional[str]
    id: str
