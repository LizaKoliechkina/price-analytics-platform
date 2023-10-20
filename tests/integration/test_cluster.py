import pytest
import requests

from .conftest import API_URL

pytestmark = pytest.mark.usefixtures('clean_up_test_objects')


@pytest.mark.parametrize(
    'name, nof_products',
    (
            ('RELAY ACCESSORIES', 4),
            ('FA ACCESSORY', 2),
            ('VALVES AND ACTUATORS', 3),
    )
)
def test_get_cluster_sales_statistics(
        name: str, nof_products: int
) -> None:
    response = requests.get(f'{API_URL}/clusters/sales_statistics/{name}')

    assert response.status_code == 200
    cluster_data = response.json()
    assert cluster_data['name'] == name
    assert len(cluster_data) == 7
    assert cluster_data['nof_products'] == nof_products


def test_get_cluster_sales_statistics_not_found() -> None:
    response = requests.get(
        f'{API_URL}/clusters/sales_statistics/NonExistentCluster',
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'No data were found for cluster: NonExistentCluster'


cluster_test_input = {
    'name': 'TestCluster',
    'description': 'Test description',
    'division': 'Test division',
    'previous_sold_quantity': 100,
}


def test_add_cluster():
    response = requests.post(f'{API_URL}/clusters/', json=cluster_test_input)
    assert response.status_code == 200
    assert response.json() == cluster_test_input


def test_add_duplicate_cluster():
    response = requests.post(f'{API_URL}/clusters/', json=cluster_test_input)
    assert response.status_code == 409
    assert response.json()['detail'] == (
        'Failed to add a new cluster because it would result '
        'in a duplicate entry in the database.'
    )


def test_update_cluster_data():
    update_data = {
        'name': 'TestCluster',
        'description': 'Updated description',
    }
    response = requests.put(f'{API_URL}/clusters/', json=update_data)
    assert response.status_code == 200
    assert response.json()['name'] == cluster_test_input['name']
    assert response.json()['description'] == update_data['description']
    assert response.json()['division'] == cluster_test_input['division']


def test_update_nonexistent_cluster():
    update_data = {
        'name': 'NonExistentCluster',
        'description': 'Updated description',
    }
    response = requests.put(f'{API_URL}/clusters/', json=update_data)
    assert response.status_code == 404
    assert response.json()['detail'] == f'Requested cluster {update_data["name"]} not found'


def test_update_no_cluster_fields():
    update_data = {
        'name': 'NonExistentCluster',
    }
    response = requests.put(f'{API_URL}/clusters/', json=update_data)
    assert response.status_code == 400
    assert response.json()['detail'] == (
        'Invalid input: At least one field must be provided for the update'
    )
