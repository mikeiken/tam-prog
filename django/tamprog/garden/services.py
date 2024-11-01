from user.models import Person
from .models import Bed, Field


class BedService:
    @staticmethod
    def rent_bed(bed_id: int, person: Person):
        try:
            bed = Bed.objects.get(id=bed_id)
            if bed.is_rented:
                return False
            bed.is_rented = True
            bed.rented_by = person
            bed.save()

            field = bed.field
            field.count_beds -= 1
            field.save()
            return True
        except Bed.DoesNotExist:
            return False

    @staticmethod
    def release_bed(bed_id: int):
        try:
            bed = Bed.objects.get(id=bed_id)
            field = bed.field
            if not bed.is_rented:
                return False
            bed.is_rented = False
            bed.rented_by = None
            bed.save()

            field.count_beds += 1
            field.save()
            return True
        except Bed.DoesNotExist:
            return False


    @staticmethod
    def get_user_beds(user):
        return Bed.objects.filter(rented_by=user)
