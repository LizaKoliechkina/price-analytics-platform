import pytest
import requests

from .conftest import API_URL


@pytest.mark.parametrize(
    'country, division, cluster',
    (
            ('France', 'HDLSD', 'RELAY ACCESSORIES'),
            ('Poland', 'HDLSD', 'FA ACCESSORY'),
    )
)
def test_get_products(country: str, division: str, cluster: str) -> None:
    response = requests.get(
        f'{API_URL}/products/{country}/{division}/{cluster}',
    )
    print(response.json())
    assert response.status_code == 200
