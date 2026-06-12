from django.template import Library

register = Library()

@register.simple_tag
def get_square(num):

    return num**2

@register.simple_tag
def allowed_roles(request,roles):

    roles = eval(roles)

    if request.user and request.user.is_authenticated and request.user.role in roles :

        return True
    
    return False