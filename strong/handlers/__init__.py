from typing import Literal, Union

from .handler_dict import handler_dict
from .handler_list import handler_list
from .handler_literal import handler_literal
from .handler_tuple import handler_tuple
from .handler_union import handler_union

HANDLERS = {
    list: handler_list,
    dict: handler_dict,
    tuple: handler_tuple,
    Literal: handler_literal,
    Union: handler_union,
}
