from django import template

register = template.Library()


@register.filter
def cool_number(value, num_decimals=2):
    """
    Django template filter to convert regular numbers to a
    cool format (ie: 2K, 434.4K, 33M...)
    :param value: number
    :param num_decimals: Number of decimal digits
    """

    int_value = int(value)
    formatted_number = '{{:.{}f}}'.format(num_decimals)
    if int_value < 1000:
        return str(int_value)
    elif int_value < 1000000:
        return formatted_number.format(int_value/1000.0).rstrip('0.') + 'k'
    else:
        return formatted_number.format(int_value/1000000.0).rstrip('0.') + 'M'

@register.filter
def get_int(value):
    a = value
    b = int(a)
    if b < 10:
        return True
    else:
        return False

@register.filter
def multiply_amount(value,amount):
    disc = float(value)
    amt = float(amount)

    v = (disc * amt)/100
    return v