from .models import Plant

class GetPlantsSortedByPrice:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Plant.objects.order_by('price' if self.ascending else '-price')