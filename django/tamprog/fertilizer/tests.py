import pytest
from .services import FertilizerService
from .models import Fertilizer
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

@pytest.mark.django_db
def test_create_fertilizer():
    # Проверяем создание удобрения через сервисный метод
    fertilizer = FertilizerService.create_fertilizer(name="Compost", boost=3, compound="Organic")
    assert fertilizer.name == "Compost"
    assert fertilizer.boost == 3
    assert fertilizer.compound == "Organic"
    assert Fertilizer.objects.filter(name="Compost").exists()


@pytest.mark.django_db
def test_get_fertilizers_for_all_plants(bed_plants, bed_plant_fertilizers):
    for bed_plant in bed_plants:
        fertilizers = FertilizerService.get_fertilizers_for_plant(bed_plant)
        expected_fertilizers = [
            bpf.fertilizer for bpf in bed_plant_fertilizers if bpf.bed_plant == bed_plant
        ]
        assert fertilizers.count() == len(expected_fertilizers), (
            f"Количество удобрений не совпадает для BedPlant с id {bed_plant.id}"
        )
        assert all(f.fertilizer in expected_fertilizers for f in fertilizers), (
            f"Некорректные удобрения для BedPlant с id {bed_plant.id}"
        )

@pytest.mark.django_db
def test_create_fertilizer_via_url_as_superuser(api_client, superuser):
    api_client.force_authenticate(user=superuser)
    url = '/api/v1/fertilizer/'
    payload = {
        "name": "BioBoost",
        "boost": 5,
        "compound": "Natural"
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_get_fertilizers_for_bed_plant_via_url(api_client, superuser, bed_plants, bed_plant_fertilizers):
    api_client.force_authenticate(user=superuser)
    bed_plant = bed_plants[0]
    url = f'/api/v1/bedfertilizer/?bed_plant={bed_plant.id}'
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK
    data = response.json()
    expected_fertilizers = [
        bpf.fertilizer.id
        for bpf in bed_plant_fertilizers
        if bpf.bed_plant.id == bed_plant.id
    ]
    assert len(data) == len(expected_fertilizers)
    for fertilizer in data:
        assert fertilizer['fertilizer'] in expected_fertilizers











