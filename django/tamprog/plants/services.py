from .models import BedPlant
from fertilizer.models import BedPlantFertilizer
from .queries import GetPlantsSortedByPrice
from fuzzywuzzy import fuzz
from rest_framework.response import Response
from rest_framework import status
from .models import Plant
from logging import getLogger

log = getLogger(__name__)

class PlantService:

    @staticmethod
    def get_sorted_plants(ascending: bool = True):
        query = GetPlantsSortedByPrice(ascending)
        log.debug(f"Getting plants sorted by price in {'ascending' if ascending else 'descending'} order")
        return query.execute()

    @staticmethod
    def fuzzy_search(query, threshold=75):
        plants = Plant.objects.all()
        query_lower = query.lower()

        exact_matches = []
        sequence_matches = []
        partial_matches = []

        for plant in plants:
            name_lower = plant.name.lower()

            if name_lower == query_lower:
                exact_matches.append((100, plant))
                continue

            if query_lower in name_lower:
                sequence_matches.append((len(query_lower), plant))
                continue

        if exact_matches or sequence_matches:
            exact_matches.sort(key=lambda x: (-x[0], x[1].name))
            sequence_matches.sort(key=lambda x: (-x[0], x[1].name))

            sorted_results = (
                [plant for _, plant in exact_matches]
                + [plant for _, plant in sequence_matches]
            )
        else:
            for plant in plants:
                name_lower = plant.name.lower()
                similarity = fuzz.partial_ratio(query_lower, name_lower)
                if similarity >= threshold:
                    partial_matches.append((similarity, plant))

            partial_matches.sort(key=lambda x: (-x[0], x[1].name))

            sorted_results = [plant for _, plant in partial_matches]

        unique_results = []
        added_ids = set()
        for plant in sorted_results:
            if plant.id not in added_ids:
                unique_results.append(plant)
                added_ids.add(plant.id)

        log.debug(f"Found {len(unique_results)} plants for query: {query}")
        return unique_results
    
    @staticmethod
    def get_suggestions(query):
        log.debug(f"Getting suggestions for query: {query}")
        return Plant.objects.filter(name__istartswith=query).values_list('name', flat=True).order_by('name')[:10]


class BedPlantService:

    @staticmethod
    def plant_in_bed(bed, plant):
        growth_time = plant.growth_time
        bed_plant = BedPlant.objects.create(bed=bed, plant=plant, growth_time=growth_time)
        log.debug(f"Plant {plant.name} planted in bed with ID={bed.id}")
        return bed_plant

    @staticmethod
    def harvest_plant(bed_plant):
        if not bed_plant:
            log.warning("Plant not found")
            return Response(
                {'error': 'Plant not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bed_plant.delete()
        log.info("Plant harvested")
        return Response(
            {'status': 'plant dug up'},
            status=status.HTTP_200_OK
        )


    @staticmethod
    def fertilize_plant(bed_plant, fertilizer):
        if not fertilizer:
            log.warning("No suitable fertilizer found")
            return Response(
                {'error': 'No suitable fertilizer found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        new_growth_time = bed_plant.growth_time - fertilizer.boost
        bed_plant.growth_time = new_growth_time
        BedPlantFertilizer.objects.create(bed_plant=bed_plant, fertilizer=fertilizer)
        bed_plant.fertilizer_applied = True
        bed_plant.save(update_fields=["fertilizer_applied", "growth_time"])
        bed_plant.save()
        log.info("Plant fertilized")
        return Response(
            {'status': 'plant fertilized'},
            status=status.HTTP_200_OK
        )


    @staticmethod
    def water_plant(bed_plant):
        log.error("Watering plants is not implemented yet")
        pass

    @staticmethod
    def dig_up_plant(bed_plant):
        if not bed_plant:
            log.warning("Plant not found")
            return Response(
                {'error': 'Plant not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bed_plant.delete()
        log.info("Plant dug up")
        return Response(
            {'status': 'plant dug up'},
            status=status.HTTP_200_OK
        )


    @staticmethod
    def filter_bed_plants(fertilizer_applied=None):
        if fertilizer_applied is not None:
            log.debug(f"Filtering bed plants by fertilizer_applied={fertilizer_applied}")
            return BedPlant.objects.filter(fertilizer_applied=fertilizer_applied)
        log.debug("Getting all bed plants")
        return BedPlant.objects.all()