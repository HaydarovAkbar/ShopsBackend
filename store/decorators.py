from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('cart')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
def allowed_user(allow_roles = []):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allow_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Bu sahifaga kirish huquqingiz yo\'q')
        return wrapper
    return decorator