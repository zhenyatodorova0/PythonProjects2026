from django import template

register = template.Library()

@register.inclusion_tag('user_info.html', takes_context=True)
def user_info(context):
    print(context)
    if context['user'].is_authenticated:
        return {
            'username': context['user'].username,
        }
    return {
        'username': 'Anonymous',
    }



# def user_info(user):
#     if user.is_authenticated:
#         return {
#             'username': user.username,
#         }
#     return {
#         'username': 'Anonymous',
#     }