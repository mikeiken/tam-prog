import pytest
from plants.services import PlantService, BedPlantService
from fertilizer.models import BedPlantFertilizer
from plants.models import BedPlant
from django.urls import reverse
from fuzzywuzzy import fuzz

@pytest.mark.django_db
def test_sort_bed_plants(api_client, user, plants):
    api_client.force_authenticate(user=user)
    url = '/api/v1/plant/?asc=true'
    response = api_client.get(url)
    assert response.status_code == 200
    response_plant_prices = [bp['price'] for bp in response.data]
    sorted_plants = sorted(plants, key=lambda bp: bp.price)
    sorted_plant_prices = [bp.price for bp in sorted_plants]
    assert response_plant_prices == sorted_plant_prices


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
def test_plant_in_bed(beds, plants):
    for bed, plant in zip(beds, plants):  # Используем zip для объединения элементов
        bed_plant = BedPlantService.plant_in_bed(bed, plant)
        assert bed_plant.bed == bed
        assert bed_plant.plant == plant
        assert bed_plant.growth_time == plant.growth_time




@pytest.mark.django_db
def test_harvest_plant(bed_plants):
    for bed_plant in bed_plants:
        BedPlantService.harvest_plant(bed_plant)
        assert not BedPlant.objects.filter(id=bed_plant.id).exists()



@pytest.mark.django_db
def test_fertilize_plant_multiple(bed_plants, fertilizers):
    for bed_plant in bed_plants:
        initial_growth_time = bed_plant.growth_time
        # Применяем удобрение
        BedPlantService.fertilize_plant(bed_plant, fertilizers[0])
        bed_plant.refresh_from_db()

        # Проверяем правильность обновления данных
        assert bed_plant.growth_time == initial_growth_time - fertilizers[0].boost
        assert bed_plant.fertilizer_applied is True

        # Проверка на наличие записи в модели BedPlantFertilizer
        assert BedPlantFertilizer.objects.filter(bed_plant=bed_plant, fertilizer=fertilizers[0]).exists()

@pytest.mark.django_db
def test_filter_bed_plants(bed_plants, fertilizers):
    # Удобрим все растения
    for bed_plant in bed_plants:
        BedPlantService.fertilize_plant(bed_plant, fertilizers[0])

    # Проверка на фильтрацию удобренных растений
    fertilized_plants = BedPlantService.filter_bed_plants(fertilizer_applied=True)
    non_fertilized_plants = BedPlantService.filter_bed_plants(fertilizer_applied=False)

    for bed_plant in bed_plants:
        if bed_plant.fertilizer_applied:
            assert bed_plant in fertilized_plants
            assert bed_plant not in non_fertilized_plants
        else:
            assert bed_plant not in fertilized_plants
            assert bed_plant in non_fertilized_plants


@pytest.mark.django_db
def test_fuzzy_search(api_client, plants, user):
    api_client.force_authenticate(user=user)
    url = '/api/v1/plant/search/'
    plant_name = plants[0].name[:3]
    response = api_client.get(url, {'q': plant_name})
    assert response.status_code == 200
    expected_matches = [
        plant.name for plant in plants
        if fuzz.ratio(plant_name.lower(), plant.name.lower()) >= 70
    ]
    response_names = [plant['name'] for plant in response.data]
    assert len(response_names) == len(expected_matches)
    assert all(name in expected_matches for name in response_names)


@pytest.mark.django_db
def test_get_suggestions(api_client, plants, user):
    api_client.force_authenticate(user=user)
    url = '/api/v1/plant/suggestions/'
    suggestion_query = plants[0].name[:1]
    response = api_client.get(url, {'q': suggestion_query})
    assert response.status_code == 200
    assert len(response.data) > 0
    assert all(suggestion_query in suggestion for suggestion in response.data)


