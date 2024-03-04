from django.shortcuts import redirect
from django.conf import settings

class SessionExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            # List of paths to exclude from redirection
            path = request.path_info.lstrip('/')
            if not any(path.startswith(exc) for exc in settings.LOGIN_EXEMPT_URLS):
                return redirect('signIn')  # Replace 'signIn' with your login route

        # Continue processing if user is authenticated or path is exempt
        return None
