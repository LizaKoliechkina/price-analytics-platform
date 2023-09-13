from typing import Optional

from pydantic import BaseModel, Field


class Cluster(BaseModel):
    name: str = Field(..., title='Product internal name', max_length=100)
    description: Optional[str] = Field(None, title='Description', max_length=300)
    division: str = Field(..., max_length=50)
    nof_products: int = Field(..., title='Number of products in the cluster')
    sold_quantity: int = Field(..., title='Quantity of products sold')
    net_sales: float = Field(
        ...,
        title='Net sales',
        description='Net value of all units sold'
    )
    sales_increase: float = Field(
        ...,
        title='Sales increase',
        description='Increase in sales compared to previous period'
    )
