from .models import Field, Bed
from user.models import Person

def create_field(name, count_beds):
    field = Field.objects.create(name=name, count_beds=count_beds)
    return field

def rent_bed(field, user):
    bed = Bed.objects.filter(field=field, is_rented=False).first()
    if bed:
        bed.is_rented = True
        bed.rented_by = user
        bed.save()
    return bed

def release_bed(bed):
    bed.is_rented = False
    bed.rented_by = None
    bed.save()
    return bed

def get_user_beds(user):
    return Bed.objects.filter(rented_by=user)
