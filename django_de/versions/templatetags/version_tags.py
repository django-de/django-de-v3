from django.template import Library

from .. import utils


register = Library()


@register.simple_tag
def latest_stable_version():
    """
    This tag returns the latest stable version as provided by github.
    """
    data = utils.get_version_data()
    if data:
        return data[0]
    return None
