from telebot.types import Message

from dataStorageBot.models import Users, Directories, Files
from dataStorageBot.utils.constants import ROOT_DIR_NAME, FileTypes


def get_user(user_id: int) -> Users:
    return Users.objects.get(user_id=user_id)


def check_root_exists(user_id: int) -> bool:
    try:
        user = get_user(user_id)
    except Users.DoesNotExist:
        user = Users.objects.create(user_id=user_id)

    try:
        Directories.objects.get(title=ROOT_DIR_NAME, user=user, parent=None)
        return True
    except Directories.DoesNotExist:
        Directories.objects.create(title=ROOT_DIR_NAME, user=user, parent=None)
        return False


def create_sub_directory(user: Users, title: str) -> None:
    Directories.objects.create(title=title, user=user, parent=user.get_current_dir())


def get_full_path(directory: Directories):
    d = directory
    full_path = d.title
    while d.parent:
        d = d.parent
        full_path = d.title + '/' + full_path
    return full_path


def get_file_id(message: Message) -> str:
    content_type = message.content_type
    if content_type == FileTypes.AUDIO.value:
        return message.audio.file_id
    elif content_type == FileTypes.DOCUMENT.value:
        return message.document.file_id
    elif content_type == FileTypes.PHOTO.value:
        return message.photo[0].file_id
    elif content_type == FileTypes.VIDEO.value:
        return message.video.file_id
    else:
        return ''


def get_send_file_func(content_type) -> str:
    if content_type == FileTypes.AUDIO.value:
        return 'send_audio'
    elif content_type == FileTypes.DOCUMENT.value:
        return 'send_document'
    elif content_type == FileTypes.PHOTO.value:
        return 'send_photo'
    elif content_type == FileTypes.VIDEO.value:
        return 'send_video'
    else:
        return ''


def create_file(message: Message):
    user = get_user(message.from_user.id)
    tg_file_id = get_file_id(message)
    if tg_file_id != '':
        Files.objects.create(title=message.caption, user=user,
                             content_type=message.content_type,
                             tg_file_id=tg_file_id, directory=user.get_current_dir())
        return True
    else:
        return False
