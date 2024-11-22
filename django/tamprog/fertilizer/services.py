from .models import Fertilizer, BedPlantFertilizer
from logging import getLogger

log = getLogger(__name__)


class FertilizerService:
    @staticmethod
    def create_fertilizer(name, boost, compound):
        fertilizer = Fertilizer.objects.create(
            name=name, boost=boost, compound=compound)
        log.debug(f'Created fertilizer: {fertilizer}')
        return fertilizer

    @staticmethod
    def get_fertilizers_for_plant(bed_plant):
        log.debug(f'Getting fertilizers for plant: {bed_plant}')
        return BedPlantFertilizer.objects.filter(bed_plant=bed_plant)
