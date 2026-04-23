from collections.abc import Callable
from types import UnionType
from typing import Literal, Union

from .handler_callable import handler_callable
from .handler_dict import handler_dict
from .handler_frozenset import handler_frozenset
from .handler_list import handler_list
from .handler_literal import handler_literal
from .handler_set import handler_set
from .handler_tuple import handler_tuple
from .handler_union import handler_union

HANDLERS = {
    list: handler_list,
    dict: handler_dict,
    tuple: handler_tuple,
    Literal: handler_literal,
    Union: handler_union,
    UnionType: handler_union,
    frozenset: handler_frozenset,
    set: handler_set,
    Callable: handler_callable,
}
