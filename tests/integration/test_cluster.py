import pytest
import requests

from .conftest import API_URL


@pytest.mark.parametrize(
    'name, nof_products',
    (
            ('RELAY ACCESSORIES', 4),
            ('FA ACCESSORY', 2),
            ('VALVES AND ACTUATORS', 3),
    )
)
def test_get_cluster_data(
        name: str, nof_products: int
) -> None:
    response = requests.get(f'{API_URL}/cluster_data/{name}')

    assert response.status_code == 200
    cluster_data = response.json()
    assert cluster_data['name'] == name
    assert len(cluster_data) == 7
    assert cluster_data['nof_products'] == nof_products


def test_get_cluster_data_not_found() -> None:
    response = requests.get(
        f'{API_URL}/cluster_data/ACCESSORY',
    )
    assert response.status_code == 404
    assert response.json() == 'No data were found for cluster: ACCESSORY'
