from .models import Worker


class GetWorkersSortedByID:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Worker.objects.order_by('id' if self.ascending else '-id')
    

class GetWorkersSortedByName:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Worker.objects.order_by('name' if self.ascending else '-name')
    

class GetWorkersSortedByPrice:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Worker.objects.order_by('price' if self.ascending else '-price')


class GetWorkersSortedByDescription:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Worker.objects.order_by('description' if self.ascending else '-description')