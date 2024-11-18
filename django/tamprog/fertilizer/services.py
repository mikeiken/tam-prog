from .models import Fertilizer, BedPlantFertilizer


class FertilizerService:
    @staticmethod
    def create_fertilizer(name, boost, compound):
        fertilizer = Fertilizer.objects.create(name=name, boost=boost, compound=compound)
        return fertilizer

    @staticmethod
    def get_fertilizers_for_plant(bed_plant):
        return BedPlantFertilizer.objects.filter(bed_plant=bed_plant)
