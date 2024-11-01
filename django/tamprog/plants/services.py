from .models import BedPlant
from fertilizer.models import BedPlantFertilizer

class BedPlantService:

    @staticmethod
    def plant_in_bed(bed, plant):
        growth_time = plant.growth_time
        bed_plant = BedPlant.objects.create(bed=bed, plant=plant, growth_time=growth_time)
        return bed_plant

    @staticmethod
    def harvest_plant(bed_plant):
        bed_plant.delete()

    @staticmethod
    def fertilize_plant(bed_plant, fertilizer):
        new_growth_time = bed_plant.growth_time - fertilizer.boost
        bed_plant.growth_time = new_growth_time
        BedPlantFertilizer.objects.create(bed_plant=bed_plant, fertilizer=fertilizer)
        bed_plant.fertilizer_applied = True
        bed_plant.save(update_fields=["fertilizer_applied", "growth_time"])
        bed_plant.save()

    @staticmethod
    def water_plant(bed_plant):
        pass

    @staticmethod
    def dig_up_plant(bed_plant):
        bed_plant.delete()
