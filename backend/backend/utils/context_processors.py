from django.conf import settings


def settings_context(_request):
    return {"settings": settings}


def support_email():
    return {"support_email_address": settings.SUPPORT_EMAIL}