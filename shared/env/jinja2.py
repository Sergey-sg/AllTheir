from crispy_forms.utils import render_crispy_form
from django.contrib.staticfiles.storage import staticfiles_storage
from jinja2 import Environment


def environment(**options):
    """
    Provides default environment for jinja.
    """
    options['cache_size'] = 0
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        "crispy": render_crispy_form,  # THIS LINE IS RELEVANT
    })
    return env
