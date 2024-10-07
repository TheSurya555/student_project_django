from .models import Traffic

class TrafficLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log traffic for each request
        Traffic.objects.create(
            user=request.user if request.user.is_authenticated else None,
            page_visited=request.path,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        response = self.get_response(request)
        return response
