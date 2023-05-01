from django.db import models

from dataStorageBot.utils.constants import *


class Directories(models.Model):
    title = models.TextField()
    parent = models.ForeignKey('self', models.CASCADE, null=True, blank=True,
                               related_name="subdirs")
    user = models.ForeignKey('dataStorageBot.Users', models.CASCADE)

    def get_title_with_emoji(self) -> str:
        return DIRECTORY_EMOJI + self.title

    class Meta:
        db_table = 'directories'


class Tags(models.Model):
    title = models.TextField()
    user = models.ForeignKey('dataStorageBot.Users', models.CASCADE)

    def get_title_with_emoji(self) -> str:
        return TAG_EMOJI + self.title

    class Meta:
        db_table = 'tags'


class Files(models.Model):
    tg_file_id = models.TextField()
    title = models.TextField()
    content_type = models.TextField()
    directory = models.ForeignKey(Directories, models.CASCADE)
    user = models.ForeignKey('dataStorageBot.Users', models.CASCADE)
    tags = models.ManyToManyField(Tags)

    def get_title_with_emoji(self) -> str:
        if self.content_type == FileTypes.AUDIO.value:
            return AUDIO_EMOJI + self.title
        elif self.content_type == FileTypes.DOCUMENT.value:
            return DOCUMENT_EMOJI + self.title
        elif self.content_type == FileTypes.PHOTO.value:
            return PHOTO_EMOJI + self.title
        elif self.content_type == FileTypes.VIDEO.value:
            return VIDEO_EMOJI + self.title
        return self.title

    class Meta:
        db_table = 'files'


class Users(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    _current_dir = models.ForeignKey(Directories, models.SET_NULL,
                                     null=True, blank=True, default=None)

    def get_root_dir(self) -> Directories:
        return Directories.objects.get(title=ROOT_DIR_NAME, user=self, parent=None)

    def get_current_dir(self) -> Directories:
        return self._current_dir or self.get_root_dir()

    class Meta:
        db_table = 'users'
