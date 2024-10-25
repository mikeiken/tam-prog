from .models import Fertilizer, BedPlantFertilizer
from plants.models import BedPlant

def create_fertilizer(name, growth_acceleration, plant):
    fertilizer = Fertilizer.objects.create(name=name, growth_acceleration=growth_acceleration, plant=plant)
    return fertilizer

def get_fertilizers_for_plant(plant):
    return Fertilizer.objects.filter(plant=plant)
