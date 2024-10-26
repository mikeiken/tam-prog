from .models import Fertilizer, BedPlantFertilizer
from plants.models import BedPlant

def create_fertilizer(name, boost, compound):
    fertilizer = Fertilizer.objects.create(name=name, boost=boost, compound=compound)
    return fertilizer

def apply_fertilizer(bed_plant, fertilizer):
    bed_plant_fertilizer = BedPlantFertilizer.objects.create(bed_plant=bed_plant, fertilizer=fertilizer)
    return bed_plant_fertilizer

def get_fertilizers_for_plant(plant):
    return Fertilizer.objects.filter(plant=plant)
