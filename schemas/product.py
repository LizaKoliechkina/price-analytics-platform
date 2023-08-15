from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class Product(BaseModel):
    name: str = Field(..., title='Product internal name', max_length=100)
    description: Optional[str] = Field(None, title='Description', max_length=300)
    global_price: float = Field(..., title='Global price')
    local_price: float = Field(..., title='Local price')
    sold_quantity: int = Field(..., title='Quantity of products sold')
    cluster: str = Field(..., max_length=50)
    division: str = Field(..., max_length=50)
    country: str = Field(..., max_length=50)

    model_config = ConfigDict(from_attributes=True)  # Pydantic v1: use class Config and from_orm
