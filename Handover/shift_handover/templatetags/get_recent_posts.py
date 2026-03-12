from django import template
from shift_handover.models import Post
register = template.Library()


class RecentPostsNode(template.Node):
    def __init__(self, posts_count: int, context_varname: str) -> None:
        self.posts_count = int(posts_count)
        self.context_varname = context_varname

    def render(self, context) -> str:
        recent_posts = Post.objects.order_by('-created_at')[:self.posts_count]
        context[self.context_varname] = recent_posts
        return ''

@register.tag
def get_recent_posts(parser, token):
    try:
        tag_name, count, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "The get_recent_posts tag excepts only three arguments"
        )
    return RecentPostsNode(count, varname)