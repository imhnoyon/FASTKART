

from djoser import email
from django.conf import settings

class CustomPasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset.txt"
    subject_template_name = "email/password_reset_subject.txt"
    html_template_name = "email/password_reset.html"

    def get_context_data(self, *args, **kwargs):
        # Djoser এর মূল context নাও
        context = super().get_context_data(*args, **kwargs)

        # user object পাওয়া
        user = context.get("user")
        if user:
            # email inject করা
            context["email"] = user.email

        # site_name যোগ করা
        context["site_name"] = getattr(settings, 'SITE_NAME', 'Backend')

        # debug print
        print("DEBUG CONTEXT KEYS:", context.keys())
        print("DEBUG EMAIL:", context.get("email"))
        print("DEBUG URL:", context.get("url"))
        print("DEBUG SITE_NAME:", context.get("site_name"))

        return context
