import logging

from django.conf import settings

from . import  get_country_by_ip, get_currency_for_country


logger = logging.getLogger(__name__)

class CountryMiddleware(object):

    def process_request(self, request):
        if 'REMOTE_ADDR' in request.META:
            request.country = get_country_by_ip(request.META['REMOTE_ADDR'])
        else:
            request.country = None


class CurrencyMiddleware(object):

    def process_request(self, request):
        if hasattr(request, 'country') and request.country is not None:
            request.currency = get_currency_for_country(request.country)
        else:
            request.currency = settings.DEFAULT_CURRENCY
