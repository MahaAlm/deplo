from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='matches_email')
def matches_email(author_email, user_email):
    return author_email == user_email