import pytest

@pytest.mark.django_db
def test_sort_bed_plants(api_client, user, bed_plants):
    api_client.force_authenticate(user=user)
    url = '/api/v1/bedplant/?asc=true'
    response = api_client.get(url)
    assert response.status_code == 200
    response_plant_ids = [bp['plant'] for bp in response.data]
    sorted_plants = sorted(bed_plants, key=lambda bp: bp.plant.name)
    sorted_plant_ids = [bp.plant.id for bp in sorted_plants]
    assert response_plant_ids == sorted_plant_ids

@pytest.mark.django_db
def test_filter_bed_plants(api_client, user, bed_plants):
    api_client.force_authenticate(user=user)

    url = '/api/v1/bedplant/?fertilizer_applied=true'
    response = api_client.get(url)
    assert response.status_code == 200
    assert all(bp['fertilizer_applied'] for bp in response.data)

    url = '/api/v1/bedplant/?fertilizer_applied=false'
    response = api_client.get(url)
    assert response.status_code == 200
    assert all(not bp['fertilizer_applied'] for bp in response.data)
