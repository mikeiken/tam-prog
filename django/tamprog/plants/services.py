from .models import Plant, BedPlant
from garden.models import Bed
from fertilizer.models import Fertilizer, BedPlantFertilizer

def plant_in_bed(bed, plant):
    bed_plant = BedPlant.objects.create(bed=bed, plant=plant)
    return bed_plant

def harvest_plant(bed_plant):
    bed_plant.delete()

def fertilize_plant(bed_plant, fertilizer):

    new_growth_time = bed_plant.growth_time - fertilizer.boost
    bed_plant.growth_time = new_growth_time

    BedPlantFertilizer.objects.create(bed_plant=bed_plant, fertilizer=fertilizer)
    bed_plant.fertilizer_applied = True
    bed_plant.save(update_fields=["fertilizer_applied", "growth_time"])
    bed_plant.save()

def water_plant(bed_plant):
    pass

def dig_up_plant(bed_plant):
    bed_plant.delete()
