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
    def create_field(name: str, all_beds: int, price: float, url: str):
        field = Field.objects.create(
            name=name,
            all_beds=all_beds,
            count_free_beds=all_beds,
            price=price,
            url=url
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
    def rent_beds(field, user, beds_count):
        free_beds = Bed.objects.filter(field=field, is_rented=False).order_by('id')[:beds_count]
        rented_beds = []
        if len(free_beds) < beds_count:
            log.warning(f"Not enough free beds available for rent.")
            return 0

        for bed in free_beds:
            bed.is_rented = True
            bed.rented_by = user
            bed.save()
            rented_beds.append(bed)

        field.count_free_beds -= beds_count
        field.save()
        log.info(f"{beds_count} beds rented successfully.")
        return beds_count

    @staticmethod
    def release_beds(field, beds_count):
        rented_beds = Bed.objects.filter(field=field, is_rented=True)[:beds_count]
        for bed in rented_beds:
            bed.is_rented = False
            bed.rented_by = None
            bed.save()

        field.count_free_beds += beds_count
        field.save()
        log.info(f"{beds_count} beds released successfully.")

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
