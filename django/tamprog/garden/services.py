from orders.models import Order
from user.models import Person
from .models import Bed
from .queries import *
from rest_framework.response import Response
from rest_framework import status
# These \/ imports for the Celery
from celery import shared_task
from celery.result import AsyncResult
from django.forms.models import model_to_dict
from django.conf import settings

from logging import getLogger

log = getLogger(__name__)

@shared_task
def get_sorted_fields_task(sort_by: str = 'id', ascending: bool = True):
    if sort_by == 'id':
        query = GetFieldsSortedByID(ascending)
    elif sort_by == 'name':
        query = GetFieldsSortedByName(ascending)
    elif sort_by == 'count_free_beds':
        query = GetFieldsSortedByCountBeds(ascending)
    elif sort_by == 'all_beds':
        query = GetFieldsSortedByCountBeds(ascending)
    elif sort_by == 'price':
        query = GetFieldsSortedByPrice(ascending)
    else:
        log.warning(f"Invalid sort_by parameter: {sort_by}")
        return []
    queryset = query.execute()
    log.debug(f"Fields sorted by {sort_by} in {'ascending' if ascending else 'descending'} order")
    return [model_to_dict(field) for field in queryset]

class FieldService:
    @staticmethod
    def create_field(name: str, all_beds: int, price: float):
        field = Field.objects.create(
            name=name,
            all_beds=all_beds,
            count_free_beds=all_beds,
            price=price,
        )
        return field

    @staticmethod 
    def get_sorted_fields(sort_by: str = 'price', ascending: bool = True):
        task = get_sorted_fields_task.delay(sort_by, ascending)
        result = AsyncResult(task.id)
        result = result.get(timeout=settings.DJANGO_ASYNC_TIMEOUT_S)
        return result
    
class BedService:
    @staticmethod
    def create_bed(field: Field, rented_by: Person = None):
        if Bed.objects.filter(field=field).count() >= field.all_beds:
            return Response(
                {"error": f"There is no space left on the field '{field.name}'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        bed = Bed.objects.create(field=field, rented_by=rented_by)
        return Response(
            {"message": "Bed successfully created."},
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def rent_bed(bed_id: int, person: Person):
        try:
            bed = Bed.objects.get(id=bed_id)

            if bed.is_rented:
                log.warning(f"Bed with ID={bed_id} is already rented.")
                return Response(
                    {"error": "This bed is already rented."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not Order.objects.filter(bed=bed, completed_at__isnull=True).exists():
                return Response(
                    {"error": "This bed can only be rented through an active order."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bed.is_rented = True
            bed.rented_by = person
            bed.save()

            field = bed.field
            field.count_free_beds -= 1
            field.save()
            log.info(f"Bed with ID={bed_id} successfully rented.")
            return Response(
                {"message": "Bed successfully rented."},
                status=status.HTTP_200_OK
            )
        except Bed.DoesNotExist as e:
            log.exception(e)
            return Response(
                {"error": "Bed with the given ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


    @staticmethod
    def release_bed(bed_id: int):
        try:
            bed = Bed.objects.get(id=bed_id)

            if Order.objects.filter(bed=bed, completed_at__isnull=True).exists():
                return Response(
                    {"error": "This bed is linked to an active order and cannot be released."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not bed.is_rented:
                log.warning(f"Bed with ID={bed_id} is not currently rented.")
                return Response(
                    {"error": "This bed is not currently rented."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            bed.is_rented = False
            bed.rented_by = None
            bed.save()

            field = bed.field
            field.count_free_beds += 1
            field.save()
            log.info(f"Bed with ID={bed_id} successfully released.")
            return Response(
                {"message": "Bed successfully released."},
                status=status.HTTP_200_OK
            )
        except Bed.DoesNotExist as e:
            log.exception(e)
            return Response(
                {"error": "Bed with the given ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


    @staticmethod
    def get_user_beds(user):
        log.debug(f"Getting beds rented by user with ID={user.id}")
        return Bed.objects.filter(rented_by=user)

    @staticmethod
    def filter_beds(is_rented=None):
        if is_rented is not None:
            log.debug(f"Filtering beds by is_rented={is_rented}")
            return Bed.objects.filter(is_rented=is_rented)
        log.debug("Getting all beds")
        return Bed.objects.all()
