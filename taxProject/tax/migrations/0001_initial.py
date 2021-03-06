# Generated by Django 2.0.2 on 2020-08-02 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='itemDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(default=None, max_length=1000, null=True)),
                ('itemCode', models.CharField(max_length=30)),
                ('itemFirstCategory', models.CharField(default=None, max_length=60, null=True)),
                ('itemFirstCategoryID', models.CharField(default=None, max_length=30, null=True)),
                ('itemSecondCategory', models.CharField(default=None, max_length=60, null=True)),
                ('itemSecondCategoryID', models.CharField(default=None, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaxDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30)),
                ('firstCategory', models.CharField(default=None, max_length=60, null=True)),
                ('FirstCategoryID', models.CharField(default=None, max_length=30, null=True)),
                ('secondCategory', models.CharField(default=None, max_length=60, null=True)),
                ('SecondCategoryID', models.CharField(default=None, max_length=30, null=True)),
                ('info', models.CharField(default=None, max_length=3000, null=True)),
            ],
        ),
    ]
