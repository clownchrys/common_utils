from typing import AnyStr

import pydantic as pyd
from pydantic import BaseModel, Field, validator
from pydantic.types import Enum
from pydantic.typing import List, Literal


class GlobalConfig:
    validate_assignment = True
    validate_all = True
    use_enum_values = True
    underscore_attrs_are_private = True


@pyd.dataclasses.dataclass(config=GlobalConfig)
class DataclassExample:
    a: int = 1


class OrderStatus(str, Enum):
    OK = 'ok'
    WAIT = 'wait'
    FAIL = 'fail'


class IndexType(int, Enum):
    type1 = 1
    type2 = 2


class Product(BaseModel):
    pid: int = Field(default=None)
    value: float = Field(default=0.)


class Order(BaseModel):
    _TYPES = Literal[
        'a',
        'b'
    ]

    oid: int = Field(default=...)
    value: float = None
    products: List[Product] = Field(default=[], max_items=5)
    literal_types: _TYPES = Field(default='a', user_defined_attr='user_defined_attr')
    enum_status: OrderStatus = Field(default=OrderStatus.OK)
    enum_index: IndexType = IndexType.type1
    description: AnyStr = ''

    class Config:
        orm_mode = True
        anystr_lower = True
        anystr_strip_whitespace = True
        

#     @validator('oid', always=True)
#     def validate_oid(cls, value, values, config, field):
#         print(value)
#         print(values)
#         print(config)
#         print(field)

#     @validator('status', always=True)
#     def validate_status(cls, value, values, config, field):
#         print(value)
#         print(values)
#         print(config)
#         print(field)
