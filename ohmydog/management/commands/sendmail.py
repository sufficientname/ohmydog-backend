from django.core.management.base import BaseCommand, CommandError
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from django.conf import settings
from django.core.mail import send_mail

EMAIL_DEFAULT_SUBJECT = "Test mail subject"
EMAIL_DEFAULT_MESSAGE = "Test mail message"

class Command(BaseCommand):
    help = "Sends a mail"
    
    def add_arguments(self, parser):
        parser.add_argument("recipient_list", nargs="+", type=str)
        parser.add_argument("-s", "--subject", nargs="?", type=str, default=EMAIL_DEFAULT_SUBJECT)
        parser.add_argument("-m", "--message", nargs="?", type=str, default=EMAIL_DEFAULT_MESSAGE)
        parser.add_argument("-f", "--from_email", nargs="?", type=str, default=settings.EMAIL_DEFAULT_FROM)


    def handle(self, *args, **kwargs):
        for email in kwargs["recipient_list"]:
            if not validate_email(email):
                raise CommandError(f"{email} is not a valid email")
        
        email = kwargs["from_email"]
        if not validate_email(email):
            raise CommandError(f"{email} is not a valid email")

        try: 
            count = send_mail(
                kwargs['subject'],
                kwargs['message'],
                kwargs['from_email'],
                kwargs['recipient_list']
            )
            self.stdout.write(self.style.SUCCESS(f"{count} mails sent"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"{str(e)}"))
        

def validate_email(email):
    try:
        EmailValidator()(email)
        return True
    except ValidationError:
        return False
