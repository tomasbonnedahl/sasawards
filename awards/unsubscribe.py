from django.contrib.auth.models import User
from django.core.signing import loads, BadSignature, dumps


def unsubscribe_url(user):
    base_url = "https://thawing-ravine-34523.herokuapp.com/unsubscribe/{}"
    # base_url = "http://127.0.0.1:7878/unsubscribe/{}"
    return base_url.format(token_from_user(user))


def token_from_user(user):
    return dumps(user.pk)


def user_from_token(token):
    try:
        user = User.objects.get(pk=loads(token))
    except (User.DoesNotExist, BadSignature):
        user = None
    return user


def unsubscribe_user(user):
    user.is_active = False
    user.save()
