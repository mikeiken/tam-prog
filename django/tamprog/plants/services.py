from .models import Plant, BedPlant
from fields.models import Bed
from fertilizers.models import Fertilizer, BedPlantFertilizer

def plant_in_bed(bed, plant):
    bed_plant = BedPlant.objects.create(bed=bed, plant=plant)
    return bed_plant

def harvest_plant(bed_plant):
    bed_plant.delete()

def fertilize_plant(bed_plant, fertilizer):
    BedPlantFertilizer.objects.create(bed_plant=bed_plant, fertilizer=fertilizer)
    bed_plant.fertilizer_applied = True
    bed_plant.save()

def water_plant(bed_plant):
    pass

def dig_up_plant(bed_plant):
    bed_plant.delete()
