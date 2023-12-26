from django.core.mail import send_mail
from django.forms import CharField, Form, Textarea
from django.template.loader import render_to_string


class FeedbackForm(Form):
    message = CharField(widget=Textarea, help_text="Введите ваш отзыв...")

    def send_email(self, user, template_name, subject, message):
        mes = render_to_string(
            template_name,
            {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "message": message,
            },
        )
        send_mail(
            subject=subject,
            message=mes,
            from_email=None,
            recipient_list=["helper.leha@gmail.com"]
        )
