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
        results = []
        plants = Plant.objects.all()
        for plant in plants:
            similarity = fuzz.ratio(query.lower(), plant.name.lower())
            if similarity >= threshold:
                results.append(plant)
        return results
    
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
