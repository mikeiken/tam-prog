
from .models import Fertilizer, BedPlantFertilizer
from plants.models import Plant

def create_fertilizer(name, boost, compound):
    fertilizer = Fertilizer.objects.create(name=name, boost=boost, compound=compound)
    return fertilizer

def get_fertilizers_for_plant(bed_plant):
    return BedPlantFertilizer.objects.filter(bed_plant=bed_plant.bed_plant)
