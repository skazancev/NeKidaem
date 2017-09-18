from django.core.exceptions import PermissionDenied


def authorized_only(view):
    def _wrap(request, *args, **kwargs):
        if request.user.is_anonymous():
            raise PermissionDenied()
        return view(request, *args, **kwargs)
    return _wrap
