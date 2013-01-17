from django import template

from .. import models


register = template.Library()


class ShowNewsToken(template.Node):
    def __init__(self, num, tmpl):
        self.tmpl = 'news/object_list.html'
        self.num = 5

        if num is not None:
            try:
                self.num = int(num)
            except ValueError:
                self.num = template.Variable(num)

        if tmpl is not None:
            if tmpl[0] in ("'", '"'):
                self.tmpl = tmpl[1:-1]
            else:
                self.tmpl = tmpl.Variable(template)

    def render(self, context):
        if isinstance(self.tmpl, template.Variable):
            template_name = self.tmpl.resolve(context)
        else:
            template_name = self.tmpl
        if isinstance(self.num, template.Variable):
            num = self.num.resolve(context)
        else:
            num = self.num

        items = models.NewsItem.objects.order_by('-pub_date')[:num]
        tmpl = template.loader.get_template(template_name)
        context.push()
        context.update({'object_list': items})
        result = tmpl.render(context)
        context.pop()

        return result


@register.tag('show_news')
def do_show_news(parser, token):
    """
    Provides a simple template tag for rendering the most recent n
    news items using a given template::

        {% show_news 5 using "news_tag.html" %}

    """
    args = token.split_contents()[1:]
    args.reverse()
    tmpl = None
    num = None

    while True:
        if not len(args):
            break

        val = args.pop()

        if val == 'using':
            try:
                tmpl = args.pop()
            except IndexError:
                raise template.TemplateSyntaxError, 'using has to be followed by a template name'
            continue

        if num is not None:
            raise template.TemplateSyntaxError, 'You can only set the template and the number of news items'

        num = val

    return ShowNewsToken(num, tmpl)
