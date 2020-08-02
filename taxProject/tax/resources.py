from import_export import resources
from .models import TaxDatabase,itemDatabase

class taxResource(resources.ModelResource):
    class Meta:
        model = TaxDatabase


class itemResource(resources.ModelResource):
    class Meta:
        model = itemDatabase