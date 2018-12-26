from django.contrib.auth.models import User
from django.core.signing import loads, BadSignature


def user_from_token(token):
    try:
        user = User.objects.get(pk=loads(token))
    except (User.DoesNotExist, BadSignature) as e:
        user = None
    return user


def unsubscribe_user(user):
    user.is_active = False
    user.save()
