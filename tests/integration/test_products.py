import pytest
import requests

from .conftest import API_URL


@pytest.mark.parametrize(
    'country, division, cluster, response_length',
    (
            ('France', 'HDLSD', 'RELAY ACCESSORIES', 4),
            ('Poland', 'HDLSD', 'FA ACCESSORY', 2),
    )
)
def test_get_products(
        country: str, division: str, cluster: str, response_length: int
) -> None:
    response = requests.get(
        f'{API_URL}/products/{country}/{division}/{cluster}',
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
