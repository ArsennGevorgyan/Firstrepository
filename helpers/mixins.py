from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from helpers.decorators import profile_decorator


class OwnProFileMixin:

    @method_decorator(login_required)
    @method_decorator(profile_decorator)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
