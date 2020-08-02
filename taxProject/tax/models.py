from django.db import models


class TaxDatabase(models.Model):
    # 商品编码
    code = models.CharField(max_length=30)
    # 大类
    firstCategory = models.CharField(max_length=60, null=True, default=None)
    # 大类id
    FirstCategoryID = models.CharField(max_length=30, null=True, default=None)
    # 小类
    secondCategory = models.CharField(max_length=60, null=True, default=None)
    # 小类id
    SecondCategoryID = models.CharField(max_length=30, null=True, default=None)
    # info
    info = models.CharField(max_length=3000, null=True, default=None)
    

class itemDatabase(models.Model):
    # item
    item = models.CharField(max_length=1000, null=True, default=None)
    # 商品编码
    itemCode = models.CharField(max_length=30)
    # 大类
    itemFirstCategory = models.CharField(max_length=60, null=True, default=None) 
    # 大类id
    itemFirstCategoryID = models.CharField(max_length=30, null=True, default=None)
    # 小类
    itemSecondCategory = models.CharField(max_length=60, null=True, default=None)
    # 小类id
    itemSecondCategoryID = models.CharField(max_length=30, null=True, default=None)

