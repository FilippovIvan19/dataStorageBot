from dataStorageBot.models import Users, Directories
from dataStorageBot.utils.constants import ROOT_DIR_NAME


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


def create_sub_directory(user: Users, name: str) -> None:
    Directories.objects.create(title=name, user=user, parent=user.get_current_dir())


def get_full_path(directory: Directories):
    d = directory
    full_path = d.title
    while d.parent:
        d = d.parent
        full_path = d.title + '/' + full_path
    return full_path
