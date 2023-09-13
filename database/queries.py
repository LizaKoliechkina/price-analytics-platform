from typing import Optional

from sqlalchemy.orm import Session

from models.product import Product
from models.cluster import Cluster


def read_products(db: Session, cluster: str, country: Optional[str] = None):
    query_filters = [Product.cluster == cluster]
    if country: query_filters.append(Product.country == country)
    products = db.query(Product).filter(*query_filters).all()
    return products


def get_cluster_division(db: Session, cluster: str):
    division = db.query(Cluster.division).filter(Cluster.name == cluster).first()
    return division[0]


def read_cluster_data(db: Session, name: str):
    cluster_data = db.query(Cluster).filter(Cluster.name == name).first()
    return cluster_data
