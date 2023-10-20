from pydantic import BaseModel, Field, ConfigDict


class CountryClusters(BaseModel):
    data: dict[str, list[str]]


class ClusterBase(BaseModel):
    name: str = Field(..., title='Cluster unique name', max_length=50)
    description: str = Field(None, max_length=300)


class ClusterInput(ClusterBase):
    division: str = Field(..., max_length=50)
    previous_sold_quantity: int = Field(
        default=0,
        ge=0,
        title='Quantity of products sold for previous period'
    )


class ClusterUpdateInput(ClusterBase):
    division: str = Field(None, max_length=50)
    previous_sold_quantity: int = Field(
        None,
        ge=0,
        title='Quantity of products sold for previous period'
    )


class Cluster(ClusterBase):
    division: str = Field(..., max_length=50)
    previous_sold_quantity: int = Field(
        ...,
        ge=0,
        title='Quantity of products sold for previous period'
    )

    model_config = ConfigDict(from_attributes=True)


class ClusterSalesData(ClusterBase):
    division: str = Field(..., max_length=50)
    nof_products: int = Field(..., ge=0, title='Number of products in the cluster')
    sold_quantity: int = Field(..., ge=0, title='Quantity of products sold')
    net_sales: float = Field(
        ...,
        ge=0.0,
        title='Net sales',
        description='Net value of all units sold'
    )
    sales_increase: float = Field(
        ...,
        title='Sales increase',
        description='Increase in sales compared to previous period'
    )
