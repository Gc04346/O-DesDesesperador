from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django_project.apps.core.models.base import has_accepted_use_terms

def user_has_accepted_use_terms(function):
    """
        Decorator pra bloquear o acesso do usuario ao sistema caso ele ainda nao tenha aceito os Termos de Uso
        Args:
            function
    """
    def wrap(request, *args, **kwargs):
        if has_accepted_use_terms(request.user.id):
            return function(request, *args, **kwargs)
        else:
            return redirect('core:homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
