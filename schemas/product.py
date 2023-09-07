from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class Product(BaseModel):
    name: str = Field(..., title='Product internal name', max_length=100)
    description: Optional[str] = Field(None, title='Description', max_length=300)
    global_price: float = Field(..., title='Global price')
    local_price: float = Field(..., title='Local price')
    sold_quantity: int = Field(..., title='Quantity of products sold')
    cluster: str = Field(..., max_length=50)
    division: str = Field(..., max_length=50)
    country: str = Field(..., max_length=50)
    net_sales: float = Field(
        ...,
        title='Net sales',
        description='Net value of all units sold'
    )
    local_deviation: float = Field(
        ...,
        title='Local deviation',
        description='Local price deviation'
    )
    sales_increase: float = Field(
        ...,
        title='Sales increase',
        description='Increase in sales compared to previous period'
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator('net_sales', 'local_deviation', 'sales_increase', mode='before')
    def round_float_to_two_decimals(cls, v: float) -> float:
        return round(v, 2)

    @field_validator('local_deviation', 'sales_increase')
    def add_percentage_sign(cls, v: float) -> str:
        return f'{v} %'
