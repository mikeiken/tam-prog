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
    elif sort_by == 'count_beds':
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
    def get_sorted_fields(sort_by: str = 'price', ascending: bool = True):
        task = get_sorted_fields_task.delay(sort_by, ascending)
        log.debug(f"Calling get_sorted_fields_task with sort_by={sort_by}, ascending={ascending}")
        log.debug(f"Waiting for the result of get_sorted_fields_task with task_id={task.id}")
        result = AsyncResult(task.id)
        result = result.get(timeout=settings.DJANGO_ASYNC_TIMEOUT_S)
        log.debug(f"get_sorted_fields_task with task_id={task.id} returned the result: {result}")
        return result
    
class BedService:
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
            bed.is_rented = True
            bed.rented_by = person
            bed.save()

            field = bed.field
            field.count_beds -= 1
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
            field = bed.field
            if not bed.is_rented:
                log.warning(f"Bed with ID={bed_id} is not currently rented.")
                return Response(
                    {"error": "This bed is not currently rented."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            bed.is_rented = False
            bed.rented_by = None
            bed.save()

            field.count_beds += 1
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
