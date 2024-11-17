import pytest
from plants.services import PlantService, BedPlantService
from fertilizer.models import BedPlantFertilizer
from plants.models import BedPlant
from django.urls import reverse


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

@pytest.mark.django_db
def test_plant_in_bed(bed, plant):
    bed_plant = BedPlantService.plant_in_bed(bed, plant)
    assert bed_plant.bed == bed
    assert bed_plant.plant == plant
    assert bed_plant.growth_time == plant.growth_time


@pytest.mark.django_db
def test_harvest_plant(bed_plant):
    BedPlantService.harvest_plant(bed_plant)
    assert not BedPlant.objects.filter(id=bed_plant.id).exists()


@pytest.mark.django_db
def test_fertilize_plant(bed_plant, fertilizer):
    initial_growth_time = bed_plant.growth_time
    BedPlantService.fertilize_plant(bed_plant, fertilizer)
    bed_plant.refresh_from_db()
    assert bed_plant.growth_time == initial_growth_time - fertilizer.boost
    assert bed_plant.fertilizer_applied is True
    assert BedPlantFertilizer.objects.filter(bed_plant=bed_plant, fertilizer=fertilizer).exists()


@pytest.mark.django_db
def test_filter_bed_plants(bed_plant, fertilizer):
    BedPlantService.fertilize_plant(bed_plant, fertilizer)
    fertilized_plants = BedPlantService.filter_bed_plants(fertilizer_applied=True)
    non_fertilized_plants = BedPlantService.filter_bed_plants(fertilizer_applied=False)

    assert bed_plant in fertilized_plants
    assert bed_plant not in non_fertilized_plants

@pytest.mark.django_db
def test_fuzzy_search(api_client, create_plants, user):
    api_client.force_authenticate(user=user)

    url = '/api/v1/plant/search/'
    response = api_client.get(url, {'q': 'ros'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Rose'


@pytest.mark.django_db
def test_get_suggestions(api_client, create_plants, user):
    api_client.force_authenticate(user=user)
    url = '/api/v1/plant/suggestions/'
    response = api_client.get(url, {'q': 't'})
    assert response.status_code == 200
    assert len(response.data) == 2
    assert 'Tulip' in response.data
    assert 'Tul' in response.data
