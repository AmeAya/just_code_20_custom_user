import random
from .models import EmailCode


def generate_email_code(email):
    # От 100000 до 999999
    while True:
        code = random.randint(100000, 999999)
        try:
            EmailCode.objects.get(code=code)
        except EmailCode.DoesNotExist:
            email_code = EmailCode(email=email, code=code)
            email_code.save()
            break
    return code
