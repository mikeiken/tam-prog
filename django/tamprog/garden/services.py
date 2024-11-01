from .models import Bed


class BedService:
    @staticmethod
    def rent_bed(field, user):
        bed = Bed.objects.filter(field=field, is_rented=False).first()
        if bed:
            bed.is_rented = True
            bed.rented_by = user
            bed.save()
        return bed

    @staticmethod
    def release_bed(bed):
        bed.is_rented = False
        bed.rented_by = None
        bed.save()
        return bed

    @staticmethod
    def get_user_beds(user):
        return Bed.objects.filter(rented_by=user)
