from django.core.mail import send_mail

from api_yamdb.settings import EMAIL


def send_message(email, code):
    return send_mail(
        subject='Код подтверждения',
        from_email=EMAIL,
        recipient_list=[email],
        message=f'Код для получения токена: {code}',
    )
