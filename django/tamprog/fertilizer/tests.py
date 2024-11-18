import pytest
from .services import FertilizerService
from .models import Fertilizer

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







