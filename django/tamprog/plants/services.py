from .models import BedPlant
from fertilizer.models import BedPlantFertilizer
from .queries import GetPlantsSortedByPrice
from fuzzywuzzy import fuzz
from rest_framework.response import Response
from rest_framework import status
from .models import Plant

class PlantService:

    @staticmethod
    def get_sorted_plants(ascending: bool = True):
        query = GetPlantsSortedByPrice(ascending)
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

        return unique_results
    
    @staticmethod
    def get_suggestions(query):
        return Plant.objects.filter(name__istartswith=query).values_list('name', flat=True).order_by('name')[:10]


class BedPlantService:

    @staticmethod
    def plant_in_bed(bed, plant):
        growth_time = plant.growth_time
        bed_plant = BedPlant.objects.create(bed=bed, plant=plant, growth_time=growth_time)
        return bed_plant

    @staticmethod
    def harvest_plant(bed_plant):
        if not bed_plant:
            return Response(
                {'error': 'Plant not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bed_plant.delete()
        return Response(
            {'status': 'plant dug up'},
            status=status.HTTP_200_OK
        )


    @staticmethod
    def fertilize_plant(bed_plant, fertilizer):
        if not fertilizer:
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
        return Response(
            {'status': 'plant fertilized'},
            status=status.HTTP_200_OK
        )


    @staticmethod
    def water_plant(bed_plant):
        pass

    @staticmethod
    def dig_up_plant(bed_plant):
        if not bed_plant:
            return Response(
                {'error': 'Plant not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bed_plant.delete()
        return Response(
            {'status': 'plant dug up'},
            status=status.HTTP_200_OK
        )


    @staticmethod
    def filter_bed_plants(fertilizer_applied=None):
        if fertilizer_applied is not None:
            return BedPlant.objects.filter(fertilizer_applied=fertilizer_applied)
        return BedPlant.objects.all()