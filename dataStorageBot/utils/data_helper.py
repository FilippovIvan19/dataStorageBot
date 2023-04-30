from dataStorageBot.models import Users, Directories
from dataStorageBot.utils.constants import ROOT_DIR_NAME


def get_user(user_id: int) -> Users:
    return Users.objects.get(user_id=user_id)


def check_root_exists(user_id: int) -> bool:
    try:
        user = get_user(user_id)
    except Users.DoesNotExist:
        user = Users(user_id=user_id)
        user.save()

    try:
        Directories.objects.get(title=ROOT_DIR_NAME, user=user, parent=None)
        return True
    except Directories.DoesNotExist:
        Directories(title=ROOT_DIR_NAME, user=user, parent=None).save()
        return False


def create_sub_directory(user: Users, name: str) -> None:
    Directories(title=name, user=user, parent=user.get_current_dir()).save()
