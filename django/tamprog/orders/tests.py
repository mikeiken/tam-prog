import pytest


@pytest.mark.django_db
def test_filter_orders(api_client, user, orders):
    api_client.force_authenticate(user=user)
    url = '/api/v1/order/'
    response = api_client.get(url, {'is_completed': 'true'})
    assert response.status_code == 200
    response_data = response.data
    assert all(order['completed_at'] is not None for order in response_data)
    assert len(response_data) == sum(1 for order in orders if order.completed_at is not None)
    response_incomplete = api_client.get(url, {'is_completed': 'false'})
    assert response_incomplete.status_code == 200
    response_data_incomplete = response_incomplete.data
    assert all(order['completed_at'] is None for order in response_data_incomplete)
    assert len(response_data_incomplete) == sum(1 for order in orders if order.completed_at is None)


