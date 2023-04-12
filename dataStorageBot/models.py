# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Directories(models.Model):
    title = models.TextField()
    parent = models.ForeignKey('self', models.CASCADE)

    class Meta:
        db_table = 'directories'


class Tags(models.Model):
    tag = models.TextField(primary_key=True)

    class Meta:
        db_table = 'tags'


class Files(models.Model):
    tg_file_id = models.TextField()
    directory = models.ForeignKey(Directories, models.CASCADE)
    tags = models.ManyToManyField(Tags)

    class Meta:
        db_table = 'files'
