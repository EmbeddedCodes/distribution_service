import time
from django.utils.deprecation import MiddlewareMixin
import math
from statistic.models import EndpointPerformance


class ResponseTimeMiddleware(MiddlewareMixin):
    """
    The ResponseTimeMiddleware class is designed to measure and record the
    response time for processing requests in a Django application. 
    At the beginning of a request, it captures the start time, and upon completing the response, 
    it calculates the elapsed time since the request started. 
    This elapsed time is then logged or saved, 
    typically for performance monitoring purposes. 
    Specifically, this middleware creates an EndpointPerformance entry for each request, 
    capturing the endpoint accessed and its response time, facilitating analysis of 
    application performance across different endpoints.
    """

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            elapsed_time = time.time() - request.start_time

            # TODO add logging
            EndpointPerformance.objects.create(
                endpoint=request.path, response_time=math.floor(elapsed_time * 1000) / 1000)
        return response
