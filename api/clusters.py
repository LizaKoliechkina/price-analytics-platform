import pandas as pd
from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from api import response_404, response_409, response_500, response_400
from calculations import percentage_increase
from database.queries import read_cluster_data, read_products
from models.cluster import Cluster as ClusterModel
from schemas.cluster import ClusterSalesData, ClusterInput, ClusterUpdateInput, Cluster

router = APIRouter()


@router.get(
    '/sales_statistics/{name}',
    response_model=ClusterSalesData,
    responses={500: response_500, 404: response_404},
)
def get_cluster_sales_statistics(
        name: str,
        request: Request,
) -> ClusterSalesData | HTTPException:
    logger.info(f'Received request to get cluster data for {name}.')
    try:
        cluster_data = read_cluster_data(request.state.db, name)
        products = read_products(request.state.db, name)
    except SQLAlchemyError:
        error_msg = f'Failed to retrieve cluster data from the database for: {name}'
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

    if not products or not cluster_data:
        error_msg = f'No data were found for cluster: {name}'
        logger.error(error_msg)
        raise HTTPException(status_code=404, detail=error_msg)

    products_df = pd.DataFrame({
        'name': p.name,
        'local_price': p.local_price,
        'sold_quantity': p.sold_quantity,
    } for p in products)
    products_df['net_sales'] = products_df['sold_quantity'] * products_df['local_price']
    total_sold_quantity = products_df['sold_quantity'].sum()
    cluster_sales_increase = percentage_increase(
        total_sold_quantity, cluster_data.previous_sold_quantity
    )

    return ClusterSalesData(
        name=cluster_data.name,
        description=cluster_data.description,
        division=cluster_data.division,
        nof_products=len(products_df['name'].unique()),
        sold_quantity=total_sold_quantity,
        net_sales=round(products_df['net_sales'].sum(), 2),
        sales_increase=cluster_sales_increase,
    )


@router.post(
    '/',
    response_model=Cluster,
    responses={500: response_500, 409: response_409},
)
def add_cluster(request: Request, body: ClusterInput) -> Cluster | HTTPException:
    logger.info(f'Received request to add new cluster.')
    db_session = request.state.db

    try:
        new_cluster = ClusterModel(**body.model_dump())
        db_session.add(new_cluster)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        error_msg = ('Failed to add a new cluster because it would result '
                     'in a duplicate entry in the database.')
        logger.error(error_msg)
        raise HTTPException(status_code=409, detail=error_msg)
    except SQLAlchemyError:
        db_session.rollback()
        error_msg = 'Failed to add a new cluster to the database'
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    db_session.refresh(new_cluster)
    return Cluster.model_validate(new_cluster)


@router.put(
    '/',
    response_model=Cluster,
    responses={500: response_500, 404: response_404, 400: response_400},
)
def update_cluster_data(
        request: Request,
        body: ClusterUpdateInput,
) -> Cluster | HTTPException:
    logger.info(f'Received request to update cluster: {body.name}.')
    if all([val is None for val in (
            body.description, body.division, body.previous_sold_quantity
    )]):
        error_msg = 'Invalid input: At least one field must be provided for the update'
        logger.error(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

    update_fields = {
        'description': body.description,
        'division': body.division,
        'previous_sold_quantity': body.previous_sold_quantity,
    }
    db_session = request.state.db

    try:
        cluster = db_session.query(ClusterModel).filter(
            ClusterModel.name == body.name
        ).first()
        if not cluster:
            error_msg = f'Requested cluster {body.name} not found'
            logger.error(error_msg)
            raise HTTPException(status_code=404, detail=error_msg)

        for field_name, new_value in update_fields.items():
            if new_value:
                setattr(cluster, field_name, new_value)
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        error_msg = f'Failed to update cluster data for {body.name}!'
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

    db_session.refresh(cluster)
    return Cluster.model_validate(cluster)
