from collections import defaultdict

from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from api import response_500
from models.product import Product
from schemas.cluster import CountryClusters

router = APIRouter()


@router.get('/cluster_list', response_model=CountryClusters, responses={500: response_500})
def get_country_clusters(request: Request) -> CountryClusters | HTTPException:
    logger.info(f'Received request to get countries cluster list.')
    try:
        db_data = request.state.db.query(
            Product.country, Product.cluster
        ).order_by(Product.country).distinct().all()
    except SQLAlchemyError:
        error_msg = f'Failed to retrieve data from the database'
        logger.error(error_msg)
        return HTTPException(status_code=500, detail=error_msg)

    country_clusters = defaultdict(list)
    for country, cluster in db_data:
        country_clusters[country].append(cluster)
    return CountryClusters(data=dict(country_clusters))
