from django.db import models

from dataStorageBot.utils.constants import ROOT_DIR_NAME


class Directories(models.Model):
    title = models.TextField()
    parent = models.ForeignKey('self', models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('dataStorageBot.Users', models.CASCADE)

    class Meta:
        db_table = 'directories'


class Tags(models.Model):
    tag = models.TextField(primary_key=True)
    user = models.ForeignKey('dataStorageBot.Users', models.CASCADE)

    class Meta:
        db_table = 'tags'


class Files(models.Model):
    tg_file_id = models.TextField()
    directory = models.ForeignKey(Directories, models.CASCADE)
    user = models.ForeignKey('dataStorageBot.Users', models.CASCADE)
    tags = models.ManyToManyField(Tags)

    class Meta:
        db_table = 'files'


class Users(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    current_dir = models.ForeignKey(Directories, models.SET_NULL,
                                    null=True, blank=True, default=None)

    def get_root_dir(self) -> Directories:
        return Directories.objects.get(title=ROOT_DIR_NAME, user=self, parent=None)

    def get_current_dir(self) -> Directories:
        cur_dir = self.current_dir
        if cur_dir:
            print('type(cur_dir)', type(cur_dir))
            return cur_dir
        else:
            return self.get_root_dir()

    class Meta:
        db_table = 'users'
