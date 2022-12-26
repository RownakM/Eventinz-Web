from currency_symbols import CurrencySymbols
from django import template
from localStoragePy import localStoragePy
localStorage=localStoragePy('eventinz.com','json')
register = template.Library()

@register.filter()
def currency_icon(value):
    symbol = CurrencySymbols.get_symbol(value)
    if symbol == None:
        symbol=value
    return symbol