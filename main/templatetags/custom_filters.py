from django import template

register = template.Library()

@register.filter
def pesos_chilenos(value):
    int_value = int(value)
    str_value = str(int_value)[::-1]
    str_value = '.'.join(str_value[i:i+3] for i in range(0, len(str_value), 3))
    str_value = '$' + str_value[::-1]
    return str_value
