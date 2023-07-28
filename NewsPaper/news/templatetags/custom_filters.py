from django import template

register = template.Library()
unwanted_words = ['temporarily', 'prosecuting', 'Parliament', 'cannabis']


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(text):
    text = text.split()
    for i, word in enumerate(text):
        if word in unwanted_words:
            text[i] = word[0] + '***'
    return ' '.join(text)
