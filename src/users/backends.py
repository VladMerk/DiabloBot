from django.contrib.auth.backends import ModelBackend

from .models import User


class DiscordBackend(ModelBackend):
    def authenticate(self, request, user: dict) -> User:
        try:
            # TODO Добавить обновление юзера, если он есть, но каких то полей не хватает
            user = User.objects.get(username=user.get("username"))
        except User.DoesNotExist:
            user = User.objects.create_user(
                id=user.get('id'),
                username=user.get("username"),
                discriminator=user.get("discriminator"),
                email=user.get("email"),
                avatar=user.get("avatar"),
                flags=user.get("flags"),
            )
            user.save()
            return user
        else:
            return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
