from .models import Field

class GetFieldsSortedByPrice:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Field.objects.order_by('price' if self.ascending else '-price')



class GetFieldsSortedByBeds:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Field.objects.order_by('count_beds' if self.ascending else '-count_beds')