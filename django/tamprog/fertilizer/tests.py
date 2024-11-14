import pytest
from .services import FertilizerService
from .models import Fertilizer, BedPlantFertilizer

@pytest.mark.django_db
def test_create_fertilizer():
    # Проверяем создание удобрения через сервисный метод
    fertilizer = FertilizerService.create_fertilizer(name="Compost", boost=3, compound="Organic")
    assert fertilizer.name == "Compost"
    assert fertilizer.boost == 3
    assert fertilizer.compound == "Organic"
    assert Fertilizer.objects.filter(name="Compost").exists()

@pytest.mark.django_db
def test_get_fertilizers_for_plant(bed_plant, bed_plant_fertilizer):
    # Проверяем получение удобрений, связанных с определенным растением
    fertilizers = FertilizerService.get_fertilizers_for_plant(bed_plant)
    assert fertilizers.count() == 1
    assert fertilizers.first().fertilizer == bed_plant_fertilizer.fertilizer