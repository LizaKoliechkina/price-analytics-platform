from sqlalchemy.orm import Session

from models.product import Product


def read_products(db: Session, country: str, division: str, cluster: str):
    products = db.query(Product).filter(
        Product.country == country,
        Product.division == division,
        Product.cluster == cluster,
    ).all()
    return products
