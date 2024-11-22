from orders.models import Order
from user.services import PersonService
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
        if not Order.objects.filter(bed=bed, completed_at__isnull=True).exists():
            return Response(
                {"error": "Planting is only allowed through an active order."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if BedPlant.objects.filter(bed=bed, plant=plant).exists():
            return Response(
                {"error": "This bed already has the specified plant."},
                status=status.HTTP_400_BAD_REQUEST
            )
        growth_time = plant.growth_time
        BedPlant.objects.create(bed=bed, plant=plant, growth_time=growth_time)
        return Response(
            {"message": "Plant successfully planted in the bed."},
            status=status.HTTP_201_CREATED
        )


    @staticmethod
    def check_and_harvest_plant(bed_plant):
        if bed_plant.is_grown:
            bed_plant.is_harvested = True
            bed_plant.save(update_fields=['is_harvested'])
            return BedPlantService.harvest_plant(bed_plant)
        return None


    @staticmethod
    def harvest_plant(bed_plant):
        if not bed_plant.is_grown:
            return Response(
                {'error': 'Plant is not fully grown yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
        bed_plant.is_harvested = True
        bed_plant.save(update_fields=['is_harvested'])
        return Response(
            {'status': 'Plant harvested'},
            status=status.HTTP_200_OK
        )


    @staticmethod
    def fertilize_plant(bed_plant, fertilizer, user):
        if not fertilizer:
            return Response(
                {'error': 'No suitable fertilizer found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if bed_plant.fertilizer_applied:
            return Response(
                {'error': 'Fertilizer can only be applied once to a plant.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        required_min_growth_time = fertilizer.boost + 5
        if bed_plant.growth_time <= required_min_growth_time:
            return Response(
                {'error':  "The plant's growth time must be at least 5 days longer than the fertilizer's boost time." },
                status=status.HTTP_400_BAD_REQUEST
            )

        balance_response = PersonService.update_wallet_balance(user, fertilizer.price)
        if balance_response.status_code != status.HTTP_200_OK:
            return balance_response

        new_growth_time = bed_plant.growth_time - fertilizer.boost
        bed_plant.growth_time = new_growth_time
        BedPlantFertilizer.objects.create(bed_plant=bed_plant, fertilizer=fertilizer)
        bed_plant.fertilizer_applied = True
        bed_plant.save(update_fields=["fertilizer_applied", "growth_time"])
        return Response(
            {'status': 'plant fertilized'},
            status=status.HTTP_200_OK
        )


    @staticmethod
    def water_plant(bed_plant):
        pass

    @staticmethod
    def dig_up_plant(bed_plant):
        if not bed_plant.is_harvested:
            return Response(
                {'error': 'Plant must be harvested before digging up'},
                status=status.HTTP_400_BAD_REQUEST
            )
        bed_plant.delete()
        return Response(
            {'status': 'Bed is now empty'},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def filter_bed_plants(fertilizer_applied=None):
        if fertilizer_applied is not None:
            return BedPlant.objects.filter(fertilizer_applied=fertilizer_applied)
        return BedPlant.objects.all()
