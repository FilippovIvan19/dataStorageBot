from django.db import models


class Users(models.Model):
    user_id = models.BigIntegerField()

    class Meta:
        db_table = 'users'


class Directories(models.Model):
    title = models.TextField()
    parent = models.ForeignKey('self', models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(Users, models.CASCADE, default=-1)

    class Meta:
        db_table = 'directories'


class Tags(models.Model):
    tag = models.TextField(primary_key=True)
    user_id = models.ForeignKey(Users, models.CASCADE, default=-1)

    class Meta:
        db_table = 'tags'


class Files(models.Model):
    tg_file_id = models.TextField()
    directory = models.ForeignKey(Directories, models.CASCADE)
    user_id = models.ForeignKey(Users, models.CASCADE, default=-1)
    tags = models.ManyToManyField(Tags)

    class Meta:
        db_table = 'files'
