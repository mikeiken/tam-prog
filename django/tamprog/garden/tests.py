import pytest

@pytest.mark.django_db
def test_sort_fields(api_client, user, fields):
    api_client.force_authenticate(user=user)
    assert len(fields) == 5
    url = '/api/v1/field/'
    response = api_client.get(url, {'sort': 'price', 'asc': 'true'})
    assert response.status_code == 200
    assert response.data
    sorted_fields = sorted(fields, key=lambda x: x.price)
    response_prices = [field['price'] for field in response.data]
    expected_prices = [field.price for field in sorted_fields]
    assert response_prices == expected_prices

@pytest.mark.django_db
def test_filter_beds(api_client, user, beds):
    api_client.force_authenticate(user=user)
    url = '/api/v1/bed/'
    response = api_client.get(url, {'is_rented': 'true'})
    assert response.status_code == 200
    rented_beds = [bed for bed in beds if bed.is_rented]
    response_rented_status = [bed['is_rented'] for bed in response.data]
    assert all(response_rented_status)
    assert len(response_rented_status) == len(rented_beds)
