from .models import Worker

class GetWorkersSortedByPrice:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Worker.objects.order_by('price' if self.ascending else '-price')