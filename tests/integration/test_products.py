import pytest
import requests

from .conftest import API_URL


@pytest.mark.parametrize(
    'country, cluster, response_length',
    (
            ('France', 'RELAY ACCESSORIES', 4),
            ('Poland', 'FA ACCESSORY', 2),
    )
)
def test_get_products(
        country: str, cluster: str, response_length: int
) -> None:
    response = requests.get(
        f'{API_URL}/products/{country}/{cluster}',
    )

    assert response.status_code == 200
    products_data = response.json()
    assert len(products_data) == response_length
    for product in products_data:
        assert len(product) == 11
        assert product['local_deviation'].split()[-1] == '%'
        assert product['sales_increase'].split()[-1] == '%'
        assert product['net_sales'] == round(
            product['sold_quantity'] * product['local_price'], 2
        )


def test_get_products_not_found() -> None:
    response = requests.get(
        f'{API_URL}/products/Franc/ACCESSORY',
    )
    assert response.status_code == 404
    assert response.json()['detail'] == (
        'No products were found for given parameters: Franc, ACCESSORY'
    )
