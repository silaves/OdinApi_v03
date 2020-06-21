from twilio.rest import Client
from django.conf import settings
from django.core.cache import cache
account_sid = settings.SMS_SSID
auth_token = settings.SMS_TOKEN

cliente = Client(account_sid, auth_token)


def _get_numbers(limite):
    numbers = []
    try:
        list_numbers = cliente.incoming_phone_numbers.list(limit=limite)
    except:
        return None
    for num in list_numbers:
        numbers.append(num.phone_number)
    return numbers

def _get_first_number():
    if cache.get('odin_number') is None:
        try:
            list_numbers = cliente.incoming_phone_numbers.list(limit=1)
        except:
            return None
        # va estar en cache 24 hrs
        cache.set('odin_number',list_numbers[0].phone_number,24*3600)
        return list_numbers[0].phone_number
    else:
        return cache.get('odin_number')


def send_pin(message, number):
    _number_from = _get_first_number()
    if _number_from is None:
        return False
    message = cliente.messages.create(
        body = message,
        from_ = 'ODIN',
        to = number
    )
    # print(message.sid)
    return True