from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import time


class CustomerSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.META['my-timing'] = time.monotonic()

    def process_response(self, request, response):
        delta_timing = (time.monotonic() - request.META['my-timing']) * 1000
        total_timing = f"{int(delta_timing)}ms"
        response.headers['X-Request-Timing'] = total_timing

        return response


# CustomerMiddleware from classwork.
# Changed logic - add initial var 'last_visit' into response and changed calculation of delta of time
class CustomerBlockSiteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        entered_times = request.session.get('entered_times')
        if entered_times:
            request.session['entered_times'] += 1
        else:
            request.session['entered_times'] = 1

    def process_response(self, request, response):
        entered_times = request.session.get('entered_times')
        last_visited = request.session.get('last_visited')

        if entered_times > 10:
            if time.monotonic() - last_visited < 15:   #swapped
                return HttpResponse("Site blocked")
            else:
                request.session['entered_times'] = 0

        request.session['last_visited'] = time.monotonic()

        return response
