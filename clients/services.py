from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from clients.models import User


def set_verify_token_and_send_mail(new_user):
    """
            Деактивировать пользователя, установить токен и сроки жизни
            TODO: отправить письмо на почту со ссылкой
        """
    now = datetime.now(pytz.timezone(settings.TIME_ZONE))

    new_user.is_active = False
    new_user.verify_token = User.objects.make_random_password(length=20)
    new_user.verify_token_expired = now + timedelta(hours=72)
    new_user.save()

    link_to_verify = reverse('users:verify_email', args=[new_user.verify_token])
    send_mail(
        subject='Подтвердите почту',
        message= f'{settings.BASE_URL}{link_to_verify}',
        recipient_list=[new_user.email],
        from_email=settings.EMAIL_HOST_USER
    )