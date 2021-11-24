from django import template

placeholder_url = 'https://via.placeholder.com/200/{bgcolor}/{fgcolor}?text={text}'

register = template.Library()


@register.filter
def placeholder_photo(obj):
    text = str(obj)
    abrev = ''.join([
        name[0] for name in
        text.split(' ')
    ])
    bgcolor = 'CCCCCCC'
    fgcolor = '0000000'
    return placeholder_url.format(text=abrev, bgcolor=bgcolor, fgcolor=fgcolor)
