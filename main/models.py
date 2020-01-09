from django.db import models


class Clients(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        db_table = 'clients'


class Projects(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    title = models.CharField(max_length=100, db_column='Title')
    client_id = models.IntegerField(db_column='Client_ID')

    class Meta:
        db_table = 'projects'


class CostTypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=100, db_column='Name')
    parent_cost_type_id = models.IntegerField(db_column='Parent_Cost_Type_ID', null=True)

    class Meta:
        db_table = 'cost_types'


class Costs(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_column='Amount')
    cost_type_id = models.IntegerField(db_column='Cost_Type_ID')
    project_id = models.IntegerField(db_column='Project_ID')

    class Meta:
        db_table = 'costs'

