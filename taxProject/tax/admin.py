from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from .models import TaxDatabase,itemDatabase

@admin.register(TaxDatabase)
class TaxDatabaseAdmin(ImportExportModelAdmin):
    list_display = ('code', 'firstCategory', 'FirstCategoryID',  
                    'secondCategory', 'SecondCategoryID', 
                    'info')

@admin.register(itemDatabase)
class itemDatabaseAdmin(ImportExportModelAdmin):
    item_list_display = ('item','code', 'firstCategory', 'FirstCategoryID ',  
                    'secondCategory', 'SecondCategoryID')
