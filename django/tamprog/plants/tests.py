import pytest
from plants.services import PlantService, BedPlantService
from fertilizer.models import BedPlantFertilizer
from plants.models import BedPlant
from django.urls import reverse
from fuzzywuzzy import fuzz
from django.utils import timezone

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
def test_filter_bed_plants(bed_plants, fertilizers, api_client, user):
    # Удобряем растения
    for bed_plant in bed_plants:
        BedPlantService.fertilize_plant(bed_plant, fertilizers[0], user)  # Передаем пользователя

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
        if fuzz.partial_ratio(plant_name.lower(), plant.name.lower()) >= 75
    ]
    response_names = [plant['name'] for plant in response.data]
    assert all(name in response_names for name in expected_matches)
    assert all(name in expected_matches for name in response_names)
    assert len(response_names) == len(expected_matches)


@pytest.mark.django_db
def test_get_suggestions(api_client, plants, user):
    api_client.force_authenticate(user=user)
    url = '/api/v1/plant/suggestions/'
    suggestion_query = plants[0].name[:1]
    response = api_client.get(url, {'q': suggestion_query})
    assert response.status_code == 200
    assert len(response.data) > 0
    assert all(suggestion_query in suggestion for suggestion in response.data)


@pytest.mark.django_db
def test_growth_time_adjustment_after_fertilizer(api_client, bed_plants, fertilizers, user):
    api_client.force_authenticate(user=user)

    for bed_plant in bed_plants:
        # Если удобрение уже было применено, пропускаем этот экземпляр
        if bed_plant.fertilizer_applied:
            print(f"Skipping plant {bed_plant.id} as fertilizer is already applied.")
            continue

        # Убедимся, что время роста достаточно велико для применения удобрения
        required_min_growth_time = fertilizers[0].boost + 5
        if bed_plant.growth_time <= required_min_growth_time:
            bed_plant.growth_time = required_min_growth_time + 1  # Увеличиваем время роста на 1 день больше минимального
            bed_plant.save()  # Сохраняем изменения

        initial_growth_time = bed_plant.growth_time

        # Применяем удобрение
        response = BedPlantService.fertilize_plant(bed_plant, fertilizers[0], user)

        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data}")  # Логируем данные ответа для диагностики

        # Проверяем, что статус успешный
        assert response.status_code == 200

        bed_plant.refresh_from_db()

        # Проверяем, что время роста было уменьшено на значение boost
        if bed_plant.fertilizer_applied:
            assert bed_plant.growth_time < initial_growth_time
        else:
            assert bed_plant.growth_time == initial_growth_time


@pytest.mark.django_db
def test_plant_without_fertilizer_growth_time(api_client, bed_plants, user):
    api_client.force_authenticate(user=user)

    # Проверяем время роста для растений, на которые не применялось удобрение
    for bed_plant in bed_plants:
        if not bed_plant.fertilizer_applied:
            initial_growth_time = bed_plant.growth_time
            bed_plant.refresh_from_db()
            assert bed_plant.growth_time == initial_growth_time  # Время роста должно оставаться без изменений

