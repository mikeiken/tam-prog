from .models import Field

class GetFieldsSortedByID:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Field.objects.order_by('id' if self.ascending else '-id')


class GetFieldsSortedByName:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Field.objects.order_by('name' if self.ascending else '-name')


class GetFieldsSortedByCountBeds:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Field.objects.order_by('count_beds' if self.ascending else '-count_beds')

class GetFieldsSortedByPrice:
    def __init__(self, ascending: bool = True):
        self.ascending = ascending

    def execute(self):
        return Field.objects.order_by('price' if self.ascending else '-price')