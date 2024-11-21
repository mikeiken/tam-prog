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
    def fuzzy_search(query, threshold=70):
        plants = Plant.objects.all()
        query_lower = query.lower()

        results = set()

        exact_matches = []
        sequence_matches = []
        unordered_matches = []
        partial_matches = []

        for plant in plants:
            name_lower = plant.name.lower()

            if name_lower == query_lower:
                exact_matches.append((100, plant))
                results.add(plant)
                continue

            if all(char in name_lower for char in query_lower):
                index_ordered = [name_lower.index(char) for char in query_lower if char in name_lower]
                if index_ordered == sorted(index_ordered):
                    sequence_matches.append((len(query_lower), plant))
                    results.add(plant)
                else:
                    unordered_matches.append((len(query_lower), plant))
                    results.add(plant)

            similarity = fuzz.partial_ratio(query_lower, name_lower)
            if similarity >= threshold:
                partial_matches.append((similarity, plant))
                results.add(plant)

        sequence_matches.sort(key=lambda x: (-x[0], x[1].name))
        unordered_matches.sort(key=lambda x: (-x[0], x[1].name))
        partial_matches.sort(key=lambda x: (-x[0], x[1].name))
        exact_matches.sort(key=lambda x: (-x[0], x[1].name))

        sorted_results = (
            [plant for _, plant in exact_matches]
            + [plant for _, plant in sequence_matches]
            + [plant for _, plant in unordered_matches]
            + [plant for _, plant in partial_matches]
        )

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