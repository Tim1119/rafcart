from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
# from celery_project import settings
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task(bind=True,name='Send Account Activation Mail to User')
def send_activation_email(self,user_id,domain):
    try:
        user = User.objects.get(id=user_id)
        mail_subject = 'Activate your Rafcart Account'
        message = render_to_string('account/mail_templates/activate_account.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(
            subject=mail_subject,
            message=strip_tags(message),
            from_email='Rafcart@ecommerce.com',
            recipient_list=[user.email],
            html_message=message,
        )
    except User.DoesNotExist:
        pass  # Handle the case where the user does not exist (optional)
