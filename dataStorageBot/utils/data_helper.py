from dataStorageBot.models import Users


def get_or_create_user(user_id):
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        user = Users(user_id=user_id)
        user.save()
    return user
